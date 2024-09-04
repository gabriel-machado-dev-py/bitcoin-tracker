from src import *


if __name__ == "__main__":
    load_dotenv()
    configure_logging()
    main()
    schedule_email()

    while True:
        schedule_time = input("The bot is programmed to run every 10 minutes, do you wish to cancel or not? (yes/no): ").lower()
        if not schedule_time.strip():
            print(f"{RED}{BOLD}Invalid option, please type 'yes' or 'no'.{RESET}")
        elif schedule_time == "yes":
            schedule.clear()
            print(f"{RED}{BOLD}The bot has been canceled.{RESET}")
            sleep(3)
            break
        elif schedule_time == "no":
            print(f"{GREEN}{BOLD}The bot will continue to run every 10 minutes.{RESET}")
            while True:
                schedule.run_pending()
                sleep(1)
        else:
            print(f"{RED}{BOLD}Invalid option, please type 'yes' or 'no'.{RESET}")
