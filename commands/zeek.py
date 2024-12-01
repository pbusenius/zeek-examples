import os
import shutil
import subprocess
from zat.log_to_dataframe import LogToDataFrame


OUTPUT_DIRECTOR = "logs"
PCAP_FILE = "data/large.pcap"


def read_files_log():
    log_to_df = LogToDataFrame()
    try:
        df = log_to_df.create_dataframe(f"{OUTPUT_DIRECTOR}/conn.log")
    except OSError:
        return

    print(df)


def execute_zeek_command():
    subprocess.run(
        [
            "zeek",
            "-C",
            "-r",
            PCAP_FILE,
            "frameworks/files/extract-all-files",
            f"Log::default_logdir={OUTPUT_DIRECTOR}",
            f"FileExtract::prefix={OUTPUT_DIRECTOR}/test",
        ]
    )


def clean_log_direcotry():
    if os.path.exists(OUTPUT_DIRECTOR):
        shutil.rmtree(OUTPUT_DIRECTOR)

    os.mkdir(OUTPUT_DIRECTOR)


def main():
    clean_log_direcotry()
    execute_zeek_command()

    read_files_log()


if __name__ == "__main__":
    main()
