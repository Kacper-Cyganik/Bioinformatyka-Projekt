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
