# Problem SBH z informacją o powtórzeniach oraz wszystkimi rodzajami błędów - implementacja algorytmu mrówkowego 

## Opis problemu
Implementacja algorytmu, który dla dowolnego spektrum, także z błędami, będzie szukać ścieżki w grafie ze spektrum o odpowiedniej długości i tym samym rekonstruować DNA z kawałków (oligonukleotydów) symulując działanie metody sekwencjonowania przed hybrydyzację.
### Dane
- Znana długość DNA (n), 
- Znana długość oligonukleotydów (k),
- Znany wierzchołek początkowy (oligonukleotyd o długości k),
- Informacja o rodzaju błędów: pozytywne / negatywne / oba rodzaje.
- Informacja jest o tym, czy danych element spektrum występuje w DNA raz, dwa razy, więcej
niż dwa razy, czyli: (1, 2, *)

## Opis rozwiązania
```
Opis algorytmu – proszę o dokładny opis, np. jeśli algorytm genetyczny, to oczekuję
dokładnego opisu jak działają krzyżowanie, mutacja i selekcja, jeśli to Tabu Search, to znowu:
jak działa lista tabu, czy jest kryterium aspiracji, czy algorytm ma jakieś sposoby radzenie
sobie z optimami lokalnymi w które TS lubi wpadać, itd. Tak samo w przypadku innych
algorytmów, zarówno tych typowych i takich bardziej autorskich – chciałbym mieć szansę
zrozumieć, jak działa algorytm bez potrzeby dokładnej analizy linia po linii kodu programu.

o Testy i wyniki testów w formie tabel i wykresów (o tym obszernie dalej, głównie od jakości tej
części będzie zależeć moja wstępna opinia / ocena projektu).
```

## Pomiary
TODO

## Wyniki
TODO


## Wnioski
TODO

## Uruchamianie
```
git clone https://github.com/Kacper-Cyganik/Bioinformatyka-Projekt.git

pip3 install -r requirements.txt

python3 main.py
```
Opis modyfikowalnych parametrów klasy ACO:
|parametr|opis|domyślna wartość|
|-|-|-|
|`alpha`|waga feromonu w wyborze mrówki|`1`|
|`beta`|waga heurystyki w wyborze mrówki|`7`|
|`colony_size`|ilość mrówek|`50`|
|`generations`|ilość generacji|`10`|
|`evaporation_rate`|współczynnik parowania feromonu|`0.65`|