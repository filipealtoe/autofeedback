# autofeedback
Python code implementing auto-generation of feedback on essays via concept map.

The project is the development of a tool to automatically generate rubric for examination types of essays based on exemplary essays and the utilization of the automatically generated rubric to provide quality and immediate feedback to students on their examination essay submissions. The generated tool is not intended to serve as a commercial application, but as a research support tool. It shall be used to further explore the topic of an artificial intelligence-driven framework for the automatic generation of high-quality feedback on examination essays to students, an open problem in the research community.

# Source Code
The top level directory contains the source code and support files for the two main applications. The two top-level python scripts are rubricgenerator.py and grading.py. The former performs the similarity analysis of all exemplary essays included in the ‘essays’ directory, generate the rubric according to the methodology explained in the final paper, and generate the corresponding concept map that represents the rubric. This script also generates a complete concept map of the generated rubric (unix1.gv.pdf) that can be found on the Source Code directory.

The latter is where the actual feedback to the student is generated. It performs similarity analysis of the student essay against the generated rubric (by the rubricgenerator.py) and creates two concept maps at the end. The first showing all good concepts (good_concepts.gv.pdf) that were captured by the student’s essay and the second showing what concepts were missed by the student (missing_concepts.gv.pdf) that should have been part of the essay. Both the generated concept map pdf files are included in the Source Code directory.

The grading script utilizes as a use case the file BadEssay.txt located in the ~/essayfeedback/grading/essays directory.
These two top level python scripts make calls to code on the specific python scripts that implement each section of functionality. Summary.py is where the concept summarization via TextRank is implemented. Similarity.py is where the concept similarity algorithms are implemented. The custom concept map generation algorithm is implemented in conceptmap.py. Visualize.py is responsible for the visualization of generated concept maps. TxtToJson.py implements some file helper methods used by the other scripts.

The full paper can be found at: 
https://drive.google.com/file/d/1lS4AYii-3iV4QB8WzaYV2DKV1njZPmEa/view?usp=sharing
