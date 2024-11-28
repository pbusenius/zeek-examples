import os
import shutil
import subprocess
from zat.log_to_dataframe import LogToDataFrame


PCAP_FILE = "data/ssh.pcap"
OUTPUT_DIRECTOR = "logs"


def read_files_log():
    log_to_df = LogToDataFrame()
    try:
        df = log_to_df.create_dataframe(f"{OUTPUT_DIRECTOR}/ssh.log")
    except OSError:
        return

    df = df.dropna(subset=["auth_success"])

    df = df[df["auth_success"] == "T"]

    df = df.reset_index()

    print(df)


def execute_zeek_command():
    subprocess.run(["zeek", "-C", "-r", PCAP_FILE, f"Log::default_logdir={OUTPUT_DIRECTOR}"])


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
