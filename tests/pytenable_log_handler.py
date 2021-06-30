import logging


def setup_logging_to_file(): {

    logging.basicConfig(filename='pyTenable_exception.log',
                        filemode='a+',
                        level=logging.DEBUG,
                        format='%(created)f - %(asctime)s - %(levelname)s - %(name)s - %(module)s - %(message)s',
                        datefmt='%d-%m-%Y:%H:%M:%S'
                        )

}


def log_exception(exception_data): {

    logging.exception(str(exception_data))

}
