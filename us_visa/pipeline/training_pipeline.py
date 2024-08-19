import sys

from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation

from us_visa.entity.config_entity import (DataIngestionConfig,
                                          DataValidationConfig)

from us_visa.entity.artifact_entity import (DataIngestionArtifact,
                                            DataValidationArtifact)

from us_visa.exception import USvisaException
from us_visa.logger import logging


class TrainPipeline:

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()

    def start_data_ingestion(self)-> DataIngestionArtifact:
        """
        This method of TrainPipeline class is responsible for starting data ingestion component
        """

        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from mongoDB")

            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Got the train set and test set from mongoDB")
            logging.info("Exited the start_data_ingestion method of TrainPipelin class")

            return data_ingestion_artifact

        except Exception as e:
            raise USvisaException(e,sys)

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        """
        This method in pipeline is responsible for starting data validation component
        """
        logging.info("Enter the start_data_validation method of TrainPipeline class")

        try:
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operatin")

            logging.info(f"Exiting start_data_validation method of TrainPipeline class")

            return data_validation_artifact

        except Exception as e :
            raise USvisaException(e,sys)


    def run_pipeline(self)-> None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        """

        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            
        except Exception as e:
            raise USvisaException(e,sys)