"""
LLM Training Dataset Management Module

This module provides a comprehensive data structure system for managing datasets used in 
Large Language Model (LLM) training, supporting both Supervised Fine-Tuning (SFT) and 
Reinforcement Learning from Human Feedback (RLHF) workflows.

## Overview
The module creates a bridge between custom data formats and HuggingFace's dataset ecosystem,
implementing two main types of training data:
1. **Instruction datasets**: For supervised fine-tuning (question-answer pairs)
2. **Preference datasets**: For RLHF training (question with preferred/rejected answers)

## Architecture
All classes inherit from VectorBaseDocument (a Pydantic model), providing:
- Automatic type validation
- JSON/dict serialization
- Vector database storage capabilities
- Consistent interface across all dataset types

## Main Components

### Dataset Types
- `DatasetType.INSTRUCTION`: Standard Q&A format for supervised learning
- `DatasetType.PREFERENCE`: Comparison format for preference learning (RLHF)

### Sample Classes (Individual Data Points)
- `InstructDatasetSample`: Single instruction-answer pair
  ```python
  sample = InstructDatasetSample(
      instruction="What is Python?",
      answer="Python is a high-level programming language..."
  )"""




from enum import Enum

from loguru import logger

try:
    from datasets import Dataset, DatasetDict, concatenate_datasets
except ImportError:
    logger.warning("Huggingface datasets not installed. Install with `pip install datasets`")


from llm_engineering.domain.base import VectorBaseDocument
from llm_engineering.domain.types import DataCategory


class DatasetType(Enum):
    INSTRUCTION = "instruction"
    PREFERENCE = "preference"


class InstructDatasetSample(VectorBaseDocument):
    instruction: str
    answer: str

    class Config:
        category = DataCategory.INSTRUCT_DATASET_SAMPLES


class PreferenceDatasetSample(VectorBaseDocument):
    instruction: str
    rejected: str
    chosen: str

    class Config:
        category = DataCategory.PREFERENCE_DATASET_SAMPLES


class InstructDataset(VectorBaseDocument):
    category: DataCategory
    samples: list[InstructDatasetSample]

    class Config:
        category = DataCategory.INSTRUCT_DATASET

    @property
    def num_samples(self) -> int:
        return len(self.samples)

    def to_huggingface(self) -> "Dataset":
        data = [sample.model_dump() for sample in self.samples]

        return Dataset.from_dict(
            {"instruction": [d["instruction"] for d in data], "output": [d["answer"] for d in data]}
        )


class TrainTestSplit(VectorBaseDocument):
    train: dict
    test: dict
    test_split_size: float

    def to_huggingface(self, flatten: bool = False) -> "DatasetDict":
        train_datasets = {category.value: dataset.to_huggingface() for category, dataset in self.train.items()}
        test_datasets = {category.value: dataset.to_huggingface() for category, dataset in self.test.items()}

        if flatten:
            train_datasets = concatenate_datasets(list(train_datasets.values()))
            test_datasets = concatenate_datasets(list(test_datasets.values()))
        else:
            train_datasets = Dataset.from_dict(train_datasets)
            test_datasets = Dataset.from_dict(test_datasets)

        return DatasetDict({"train": train_datasets, "test": test_datasets})


class InstructTrainTestSplit(TrainTestSplit):
    train: dict[DataCategory, InstructDataset]
    test: dict[DataCategory, InstructDataset]
    test_split_size: float

    class Config:
        category = DataCategory.INSTRUCT_DATASET


class PreferenceDataset(VectorBaseDocument):
    category: DataCategory
    samples: list[PreferenceDatasetSample]

    class Config:
        category = DataCategory.PREFERENCE_DATASET

    @property
    def num_samples(self) -> int:
        return len(self.samples)

    def to_huggingface(self) -> "Dataset":
        data = [sample.model_dump() for sample in self.samples]

        return Dataset.from_dict(
            {
                "prompt": [d["instruction"] for d in data],
                "rejected": [d["rejected"] for d in data],
                "chosen": [d["chosen"] for d in data],
            }
        )


class PreferenceTrainTestSplit(TrainTestSplit):
    train: dict[DataCategory, PreferenceDataset]
    test: dict[DataCategory, PreferenceDataset]
    test_split_size: float

    class Config:
        category = DataCategory.PREFERENCE_DATASET


def build_dataset(dataset_type, *args, **kwargs) -> InstructDataset | PreferenceDataset:
    if dataset_type == DatasetType.INSTRUCTION:
        return InstructDataset(*args, **kwargs)
    elif dataset_type == DatasetType.PREFERENCE:
        return PreferenceDataset(*args, **kwargs)
    else:
        raise ValueError(f"Invalid dataset type: {dataset_type}")
