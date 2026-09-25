import json


class Cennik:
    def __init__(self, nazwa_pliku):
        self.nazwa_pliku = nazwa_pliku
        self.zawartosc = self.pobierz_dane()

    def pobierz_dane(self):
        try:
            with open(self.nazwa_pliku, "r", encoding="utf-8") as plik:
                return json.load(plik)
        except FileNotFoundError:
            print("Błąd: Nie znaleziono pliku cennik.json!")
            return None


class Koszyk:
    def __init__(self):
        self.elementy = []

    def dodaj(self, nazwa_biletu, cena_biletu):
        self.elementy.append({
            "nazwa": nazwa_biletu,
            "cena": cena_biletu
        })

    def pokaz(self):
        if len(self.elementy) == 0:
            print("\nKoszyk jest pusty.")
            return 0

        laczna_kwota = 0

        print("\n--- TWÓJ KOSZYK ---")

        for pozycja in self.elementy:
            print(f"- {pozycja['nazwa']}: {pozycja['cena']:.2f} PLN")
            laczna_kwota += pozycja["cena"]

        print(f"RAZEM: {laczna_kwota:.2f} PLN")

        return laczna_kwota

    def usun_wszystko(self):
        self.elementy.clear()


class AutomatBiletowy:
    def __init__(self):
        self.cennik = Cennik("cennik.json")
        self.koszyk = Koszyk()
        self.wybrane_poziomy = []

    def pobierz_wybor(self, tekst):
        while True:
            wybor = input(tekst).strip().lower()

            if len(wybor) == 1:
                return wybor

            print("Błąd: Wpisz tylko jeden znak!")

    def platnosc(self, kwota_do_zaplaty):
        print(f"\nDo zapłaty: {kwota_do_zaplaty:.2f} PLN")

        pozostalo = kwota_do_zaplaty

        while True:
            try:
                podana_kwota = float(
                    input("Wrzuć pieniądze (podaj kwotę): ")
                )

                if podana_kwota < pozostalo:
                    pozostalo -= podana_kwota

                    print(
                        f"Niewystarczająca kwota. "
                        f"Brakuje {pozostalo:.2f} PLN"
                    )

                else:
                    reszta = podana_kwota - pozostalo

                    print(
                        f"Dziękujemy! Wydaję resztę: "
                        f"{reszta:.2f} PLN"
                    )

                    print("Bilety zostały wydrukowane.")
                    return

            except ValueError:
                print("Błąd: Podaj poprawną liczbę!")

    def znajdz_poziom(self):
        aktualny_poziom = self.cennik.zawartosc

        for element in self.wybrane_poziomy:
            aktualny_poziom = aktualny_poziom[element]

        return aktualny_poziom

    def pokaz_menu(self, aktualny_poziom):
        if self.wybrane_poziomy:
            nazwa_menu = " / ".join(self.wybrane_poziomy).upper()
        else:
            nazwa_menu = "START"

        print(f"\n--- MENU: {nazwa_menu} ---")

        mapa_opcji = {}

        for numer, nazwa in enumerate(aktualny_poziom, start=1):
            klawisz = str(numer)
            mapa_opcji[klawisz] = nazwa

            wartosc = aktualny_poziom[nazwa]

            if isinstance(wartosc, (int, float)):
                print(f"[{klawisz}] {nazwa} ({wartosc} PLN)")
            else:
                print(f"[{klawisz}] {nazwa}")

        print("[K] Zobacz koszyk i zapłać")
        print("[R] Resetuj wybór")
        print("[X] Wyjdź")

        return mapa_opcji

    def obsluz_koszyk(self):
        suma = self.koszyk.pokaz()

        if suma <= 0:
            return

        decyzja = self.pobierz_wybor(
            "Czy chcesz zapłacić? (t/n): "
        )

        if decyzja == "t":
            self.platnosc(suma)
            self.koszyk.usun_wszystko()
            self.wybrane_poziomy.clear()

    def uruchom(self):
        if self.cennik.zawartosc is None:
            return

        while True:
            aktualny_poziom = self.znajdz_poziom()

            opcje = self.pokaz_menu(aktualny_poziom)

            wybor = self.pobierz_wybor("Wybór: ")

            if wybor == "x":
                break

            elif wybor == "r":
                self.wybrane_poziomy.clear()

            elif wybor == "k":
                self.obsluz_koszyk()

            elif wybor in opcje:
                nazwa = opcje[wybor]
                wartosc = aktualny_poziom[nazwa]

                if isinstance(wartosc, dict):
                    self.wybrane_poziomy.append(nazwa)

                else:
                    pelna_nazwa = " ".join(
                        self.wybrane_poziomy + [nazwa]
                    )

                    self.koszyk.dodaj(
                        pelna_nazwa,
                        wartosc
                    )

                    print(f"DODANO: {nazwa}")

                    self.wybrane_poziomy.clear()


if __name__ == "__main__":
    program = AutomatBiletowy()
    program.uruchom()