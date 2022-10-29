Project for combinatorial optimization

#Projekt Optymalizacja Kombinatoryczna: Maksymalna ilość dziur w bloku sera, s151918

Przyjmując uproszczony model sera, składający się z połączonych z sobą kul: Ile można maksymalnie wyjąć kul z bloku sera, aby ten strukturalnie był w stanie się utrzymać?

#Ograniczenia

Struktura sera zniesie ubytek kul, pod warunkiem, że każda z pozostałych kul będzie spełniać co najmniej jeden z poniższych warunków:
  * Kula jest połączona z co najmniej trzema innymi
  * Kula jest połączona z jedną inną kulą, pod warunkiem, że tamta jest połączona z co najmniej czterema innymi
  * Kula jest połączona z dwiema innymi kulami, pod warunkiem, że każda z tych jest połączona z co najmniej czterema innymi.

Projekt zakłada: 
  * Generację grafu reprezentującego blok (prostopadłościan) sera
  * Algorytm typu //bruteforce// generujący dziury w grafie sera (otrzymany graf musi być spójny)
  * Trójwymiarowa wizualizacja wygenerowanego "dziurawego" grafu za pomocą oprogramowania //Blender// (?)
