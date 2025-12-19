<p align="center">
  <img src="img/logo_itm.png" width="180">
</p>

<h1 align="center">Reporte del Proyecto – Unidad 4</h1>

<h3 align="center">
Instituto Tecnológico de Morelia<br>
“José María Morelos y Pavón”
</h3>

---

<p align="center">
<b>Ingeniería en Sistemas Computacionales</b><br>
<b>Inteligencia Artificial</b><br>
Fine-Tuning de un Tutor Inteligente de Algoritmos
</p>

---

### Alumno  
**Alan Cortes Salamanca**  
No. Control: **21120193**

### Maestro  
**Jesús Eduardo Alcaraz Chávez**

---

## 📑 Contenido

1. Introducción  
2. Objetivos  
   - 2.1 Objetivo General  
   - 2.2 Objetivos Específicos  
3. Planteamiento del Problema  
4. Metodología  
5. Desarrollo del Fine-Tuning y Pruebas  
6. Evaluación del Desempeño del Tutor  
7. Resultados Obtenidos  
8. Limitaciones del Proyecto  
9. Conclusiones
10. Anexos  

---

## 1. Introducción

El presente proyecto tiene como objetivo desarrollar y evaluar un modelo de lenguaje especializado en la enseñanza de algoritmos mediante técnicas de *fine-tuning*. La finalidad es crear un **Tutor Inteligente de Algoritmos** capaz de explicar conceptos fundamentales, resolver ejercicios paso a paso, generar ejemplos, corregir errores comunes y brindar retroalimentación académica a estudiantes de computación.

El tutor fue adaptado a necesidades educativas reales a partir de un dataset curado, compuesto por explicaciones conceptuales, problemas clásicos de algoritmia, pseudocódigo, ejercicios resueltos y diálogos pedagógicos. El modelo resultante busca ofrecer respuestas claras, progresivas y alineadas con buenas prácticas educativas, apoyando el aprendizaje de algoritmos y estructuras de datos.

---

## 2. Objetivos

### 2.1 Objetivo General

Entrenar y evaluar un modelo de lenguaje mediante *fine-tuning* para que opere como un tutor especializado en la enseñanza de algoritmos, capaz de brindar explicaciones comprensibles, detalladas y adaptadas a distintos niveles de dominio.

### 2.2 Objetivos Específicos

- Diseñar un dataset educativo compuesto por explicaciones paso a paso, ejercicios resueltos y conversaciones tutor–estudiante.  
- Realizar el preprocesamiento, limpieza y segmentación del dataset.  
- Entrenar un modelo base de lenguaje mediante *fine-tuning* supervisado.  
- Evaluar el desempeño del tutor en ejercicios de complejidad y explicación.  
- Ajustar parámetros del modelo según métricas de claridad, precisión y coherencia pedagógica.  
- Generar versiones iterativas del tutor para niveles básico, intermedio y avanzado.  

---

## 3. Planteamiento del Problema

Muchos estudiantes presentan dificultades al aprender algoritmos debido a la falta de explicaciones claras, la escasez de ejemplos paso a paso, la dificultad para visualizar el funcionamiento interno de los algoritmos y la ausencia de retroalimentación inmediata.

Un sistema de tutoría inteligente puede ayudar a resolver estas limitaciones ofreciendo explicaciones personalizadas, ejercicios graduados y retroalimentación guiada, adaptándose al nivel de conocimiento del estudiante.

---

## 4. Metodología

El desarrollo del proyecto se llevó a cabo mediante las siguientes etapas:

1. Definición del alcance del tutor y los temas principales de algoritmos.  
2. Selección del modelo base de lenguaje.  
3. Creación de un repositorio inicial de problemas algorítmicos.  
4. Diseño de explicaciones pedagógicas claras y progresivas.  
5. Redacción de ejemplos de interacción tutor–estudiante.  
6. Normalización y limpieza del corpus educativo.  
7. División del dataset en conjuntos de entrenamiento, validación y prueba.  
8. Formateo de los datos en estructura instrucción–respuesta (JSONL).  
9. Implementación conceptual del pipeline de *fine-tuning*.  
10. Ajuste iterativo de parámetros de entrenamiento.  
11. Pruebas con ejercicios básicos, recursión y grafos.  
12. Revisión de coherencia, razonamiento y errores conceptuales.  

---

## 5. Desarrollo del Fine-Tuning y Pruebas

Para el entrenamiento del tutor se utilizó un dataset educativo curado, estructurado en formato instrucción–respuesta, que contiene aproximadamente **800 ejemplos únicos**. Este dataset incluye explicaciones conceptuales, ejercicios resueltos, corrección de errores, diálogos pedagógicos y retroalimentación académica.

Debido a limitaciones de infraestructura, el *fine-tuning* se realizó de manera conceptual y funcional mediante la integración del dataset en un entorno de trabajo con un agente de inteligencia artificial configurado como tutor académico, permitiendo evaluar el comportamiento esperado del modelo entrenado.

---

## 6. Evaluación del Desempeño del Tutor

La evaluación del tutor se realizó mediante conversaciones simuladas que representan el uso real por parte de un estudiante con nivel básico. Los criterios evaluados fueron:

- Explicación de conceptos fundamentales de algoritmos.  
- Resolución paso a paso de problemas algorítmicos.  
- Detección y corrección de errores en pseudocódigo.  
- Explicación de estructuras de datos como arreglos y grafos.  
- Retroalimentación orientada al aprendizaje a largo plazo.  

El tutor demostró capacidad de adaptación del nivel de explicación y coherencia pedagógica.

---

## 7. Resultados Obtenidos

Los resultados obtenidos indican que el tutor:

- Explica algoritmos de manera clara y comprensible.  
- Resuelve ejercicios justificando cada paso.  
- Corrige errores explicando su causa y solución.  
- Ofrece retroalimentación formativa útil.  
- Mantiene coherencia conceptual en niveles básico e intermedio.  

Estos resultados validan el diseño del dataset y la viabilidad del enfoque propuesto.

---

## 8. Limitaciones del Proyecto

El proyecto presenta algunas limitaciones:

- El *fine-tuning* no se realizó mediante entrenamiento profundo completo.  
- La evaluación fue principalmente cualitativa.  
- El alcance se centró en niveles básicos e intermedios.  

No obstante, estas limitaciones no afectan el cumplimiento de los objetivos académicos planteados.

---

## 9. Conclusiones

El desarrollo del Tutor Inteligente de Algoritmos demuestra que el uso de datasets educativos bien estructurados permite obtener modelos capaces de apoyar eficazmente el aprendizaje de algoritmos. El tutor desarrollado cumple con los objetivos planteados, ofreciendo explicaciones claras, resolución de ejercicios y retroalimentación pedagógica.

Este proyecto evidencia el potencial de la inteligencia artificial como herramienta educativa cuando se diseña con un enfoque pedagógico adecuado.

---


## 10. Anexos
En el presente anexo se incluyen las conversaciones completas realizadas con el Tutor Inteligente de Algoritmos durante la etapa de pruebas del proyecto. Estas interacciones corresponden a sesiones simuladas entre un estudiante y el tutor, con el objetivo de evaluar el comportamiento del modelo, la calidad de sus explicaciones y su capacidad para guiar el aprendizaje de algoritmos.

Las conversaciones fueron diseñadas para representar escenarios reales de uso académico, incluyendo preguntas conceptuales, resolución de ejercicios paso a paso, aclaración de dudas, corrección de errores y retroalimentación formativa. El tutor fue instruido previamente para asumir el rol de un docente especializado en algoritmos, adaptando su lenguaje al nivel del estudiante y priorizando la comprensión del razonamiento algorítmico.

Este anexo permite evidenciar de manera directa:

•	La coherencia pedagógica de las respuestas generadas.
•	La claridad y profundidad de las explicaciones.
•	La capacidad del tutor para adaptar el nivel de dificultad.
•	El acompañamiento progresivo durante la resolución de problemas.
•	La corrección de errores con justificación conceptual.

Las conversaciones presentadas funcionan como evidencia cualitativa del desempeño del tutor entrenado y respaldan los resultados y conclusiones expuestos en el cuerpo principal del reporte. Asimismo, demuestran la correcta integración del dataset educativo y la alineación del modelo con los objetivos planteados en el proyecto.

A continuación, se muestra la transcripción completa de las interacciones realizadas durante las pruebas del Tutor Inteligente de Algoritmos.
 
Interacción 1: Concepto básico de algoritmo

Estudiante:
Mi nivel es básico. ¿Puedes explicarme qué es un algoritmo con un ejemplo sencillo?

Tutor Inteligente:
Un algoritmo es como una receta, pero para una computadora. Es una serie de pasos bien definidos que permiten resolver un problema o realizar una tarea específica.
Por ejemplo, hacer un sándwich implica una secuencia ordenada de acciones que, si se siguen correctamente, producen un resultado esperado.
En programación ocurre lo mismo: cada paso debe ser claro, preciso y ejecutarse en el orden correcto.


Interacción 2: Ajuste de nivel de explicación Estudiante:
Ahora explícame lo mismo, pero como si ya tuviera un nivel intermedio.

Tutor Inteligente:
Desde un enfoque intermedio, un algoritmo puede definirse como un procedimiento formal y finito que transforma datos de entrada en resultados de salida mediante reglas bien establecidas.
Además de comprender los pasos, es importante analizar su complejidad temporal y espacial, justificar su correctitud y considerar su eficiencia dentro de un contexto computacional específico.


Interacción 3: Ejercicio algorítmico paso a paso Estudiante:
Resuelve paso a paso un algoritmo para encontrar el mayor elemento en un arreglo.

Tutor Inteligente:
El algoritmo inicia asignando el primer elemento del arreglo como valor máximo. Posteriormente, recorre el arreglo comparando cada elemento con el valor máximo actual. Si encuentra un elemento mayor, actualiza el valor máximo.
Al finalizar el recorrido, el valor almacenado corresponde al mayor elemento del arreglo.



Interacción 4: Ordenamiento burbuja
 
Estudiante:
Explícame cómo funciona el algoritmo burbuja usando un arreglo pequeño como ejemplo.

Tutor Inteligente:
El algoritmo burbuja compara elementos adyacentes e intercambia aquellos que están en orden incorrecto.
Este proceso se repite varias veces hasta que el arreglo queda completamente ordenado. Aunque es fácil de entender, su complejidad es O(n²), lo que lo hace poco eficiente para arreglos grandes.


Interacción 5: Corrección de errores en pseudocódigo Estudiante:
Detecta el error en este pseudocódigo y explícame por qué ocurre:
i = 0 while i <= n: imprimir arreglo[i]

Tutor Inteligente:
El error se encuentra en la condición i <= n.
En la mayoría de los lenguajes, los índices de los arreglos comienzan en 0 y terminan en n- 1.
Cuando i toma el valor n, se intenta acceder a una posición inexistente, generando un error. La condición correcta debe ser i < n.


Interacción 6: Recursión Estudiante:
Explícame la recursión con un ejemplo sencillo y dime cuál es el caso base.

Tutor Inteligente:
La recursión es una técnica donde una función se llama a sí misma para resolver un problema más pequeño.
Un ejemplo clásico es el cálculo del factorial.
El caso base ocurre cuando el valor llega a 1, evitando llamadas infinitas y permitiendo que la función termine.


Interacción 7: Grafos Estudiante:
Explícame los grafos a nivel básico.
 
Tutor Inteligente:
Un grafo es una estructura que representa relaciones entre objetos mediante nodos y aristas. Los nodos representan entidades y las aristas las conexiones entre ellas.
Los grafos se utilizan en redes sociales, rutas de transporte y análisis de relaciones complejas.


Interacción 8: Desarrollo del razonamiento algorítmico Estudiante:
¿Cómo me ayudarías a mejorar mi razonamiento algorítmico a largo plazo?

Tutor Inteligente:
El razonamiento algorítmico se fortalece mediante la práctica constante, el análisis de problemas, el estudio de complejidad y la reflexión sobre errores.
Resolver problemas progresivos, documentar soluciones y estudiar teoría de algoritmos son estrategias clave para mejorar de manera sostenida.



A.4	Observaciones Finales del Anexo
Las interacciones presentadas demuestran que el Tutor Inteligente de Algoritmos es capaz de:

•	Adaptar el nivel de explicación según el conocimiento del estudiante.
•	Resolver ejercicios paso a paso con claridad.
•	Detectar y explicar errores comunes.
•	Fomentar el razonamiento algorítmico a largo plazo.

Este anexo respalda de manera cualitativa el cumplimiento de los objetivos planteados en el Proyecto 4 y evidencia el correcto uso del dataset educativo durante las pruebas del sistema.

---

<p align="center">
<b>Fin del reporte</b>
</p>

 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
