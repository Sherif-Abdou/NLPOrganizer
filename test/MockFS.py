import os
import os.path as path
from shutil import rmtree


def generate_mock_folder():
	if path.exists(path.join(path.dirname(__file__), "mock")):
		rmtree("mock")
	os.mkdir("mock")
	with open("mock/a.txt", "w") as a:
		a.write("World War I (often abbreviated as WWI or WW1), also known as the First World War or the Great War, was a global war originating in Europe that lasted from 28 July 1914 to 11 November 1918. Contemporaneously described as the war to end all wars,[8] it led to the mobilisation of more than 70 million military personnel, including 60 million Europeans, making it one of the largest wars in history.[9][10] It is also one of the deadliest conflicts in history,[11] with an estimated nine million combatants and seven million civilian deaths as a direct result of the war, while resulting genocides and the resulting 1918 influenza pandemic caused another 50 to 100 million deaths worldwide.[12]")
	with open("mock/b.txt", "w") as b:
		b.write("Seven Years’ War, (1756–63), the last major conflict before the French Revolution to involve all the great powers of Europe. Generally, France, Austria, Saxony, Sweden, and Russia were aligned on one side against Prussia, Hanover, and Great Britain on the other. The war arose out of the attempt of the Austrian Habsburgs to win back the rich province of Silesia, which had been wrested from them by Frederick II (the Great) of Prussia during the War of the Austrian Succession (1740–48). But the Seven Years’ War also involved overseas colonial struggles between Great Britain and France, the main points of contention between those two traditional rivals being the struggle for control of North America (the French and Indian War; 1754–63) and India. With that in mind, the Seven Years’ War can also be seen as the European phase of a worldwide nine years’ war fought between France and Great Britain. Britain’s alliance with Prussia was undertaken partly in order to protect electoral Hanover, the British ruling dynasty’s Continental possession, from the threat of a French takeover.")
	with open("mock/c.ab.txt", "w") as b:
		b.write("Hello Land this is a test thing #3.\nIt's a pretty quality test thing.")
