import os
import shutil
import subprocess
import tempfile

from loguru import logger

from llm_engineering.domain.documents import RepositoryDocument

from .base import BaseCrawler

class GithubCrawler(BaseCrawler):
    model = RepositoryDocument

    def __init__(self, ignore=(".git", ".toml", ".lock", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg", ".dll", ".exe", ".zip", ".tar", ".gz", ".pdf", ".docx", ".xlsx"), max_file_size_mb=0.5) -> None:
        super().__init__()
        self._ignore = ignore
        self._max_file_size = max_file_size_mb * 1024 * 1024  # Convert to bytes (500KB per file)

    def extract(self, link: str, **kwargs) -> None:
        old_model = self.model.find(link=link)
        if old_model is not None:
            logger.info(f"Repository already exists in the database: {link}")
            return

        logger.info(f"Starting scrapping Github repository: {link}")

        repo_name = link.strip("/").split("/")[-1]
        local_temp = tempfile.mkdtemp()

        try:
            os.chdir(local_temp)
            subprocess.run(["git", "clone", link])
            
            repo_path = os.path.join(local_temp, repo_name)

            tree = {}
            total_size = 0
            files_processed = 0
            files_skipped = 0
            
            # Priority file extensions (code files we definitely want)
            priority_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.r', '.sql', '.html', '.css', '.scss', '.less', '.vue', '.jsx', '.tsx', '.md', '.txt', '.yml', '.yaml', '.json', '.xml', '.sh', '.bat', '.ps1', '.dockerfile', '.nf']
            
            for root, _, files in os.walk(repo_path):
                dir_path = root.replace(repo_path, "").lstrip("/")
                
                # Skip ignored directories
                if any(dir_path.startswith(ignore) for ignore in self._ignore):
                    continue
                
                # Skip common large directories
                if any(skip_dir in dir_path.lower() for skip_dir in ['node_modules', 'venv', '__pycache__', '.venv', 'build', 'dist', 'target']):
                    continue

                # Sort files by priority (code files first)
                sorted_files = sorted(files, key=lambda f: (
                    0 if any(f.lower().endswith(ext) for ext in priority_extensions) else 1,
                    f.lower()
                ))

                for file in sorted_files:
                    # Skip ignored file types
                    if any(file.endswith(ignore) for ignore in self._ignore):
                        files_skipped += 1
                        continue
                        
                    file_full_path = os.path.join(root, file)
                    
                    # Check file size before reading
                    try:
                        file_size = os.path.getsize(file_full_path)
                        if file_size > self._max_file_size:
                            logger.debug(f"Skipping large file {file} ({file_size / 1024:.1f}KB)")
                            files_skipped += 1
                            continue
                    except OSError:
                        files_skipped += 1
                        continue
                    
                    # Stop if approaching MongoDB document limit (keep under 5MB total)
                    if total_size > 5 * 1024 * 1024:
                        logger.info(f"Stopping extraction - document size limit reached ({total_size / 1024 / 1024:.1f}MB)")
                        break
                    
                    file_path = os.path.join(dir_path, file) if dir_path else file
                    try:
                        with open(file_full_path, "r", errors="ignore") as f:
                            content = f.read()
                            
                            # Skip if content is too large
                            if len(content) > self._max_file_size:
                                logger.debug(f"Skipping large content {file} ({len(content) / 1024:.1f}KB)")
                                files_skipped += 1
                                continue
                            
                            # Clean content (remove excessive whitespace, keep structure)
                            content = content.replace(",", "").strip()
                            if content:  # Only add non-empty files
                                tree[file_path] = content
                                total_size += len(content)
                                files_processed += 1
                                
                    except Exception as e:
                        logger.debug(f"Could not read file {file_path}: {e}")
                        files_skipped += 1
                
                # Break outer loop if size limit reached
                if total_size > 5 * 1024 * 1024:
                    break

            logger.info(f"Repository {repo_name}: processed {files_processed} files, skipped {files_skipped} files, total size: {total_size / 1024 / 1024:.2f}MB")

            user = kwargs["user"]
            instance = self.model(
                content=tree,
                name=repo_name,
                link=link,
                platform="github",
                author_id=user.id,
                author_full_name=user.full_name,
            )
            instance.save()

        except Exception as e:
            logger.error(f"Error extracting repository {link}: {e}")
            raise
        finally:
            try:
                shutil.rmtree(local_temp)
            except Exception as e:
                logger.warning(f"Could not clean up temp directory: {e}")

        logger.info(f"Finished scrapping Github repository: {link}")
