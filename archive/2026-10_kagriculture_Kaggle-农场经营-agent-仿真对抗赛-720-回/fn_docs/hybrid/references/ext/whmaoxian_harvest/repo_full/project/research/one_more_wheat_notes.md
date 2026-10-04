# Kaggriculture: One More Wheat

A small improvement to the Metav4 + Pipe16 agent: let the temporary opening
wheat crop grow one extra day, then harvest **three wheat instead of two**.

An idle worker harvests and delivers the crop, restoring the pasture before
the cow arrives. No extra land or workers are needed.


## Run

Run all cells to create `submission.tar.gz`, then select that file when
submitting to Kaggriculture. The agent is self-contained and runs on CPU.


## Credits

Based on [Thomas Tschinkel's Metav4 Farm](https://www.kaggle.com/code/thomastschinkel/the-metav4-farm-submission-v13),
[Nathan Jacob's Pipe16](https://www.kaggle.com/code/nathanjacob/kaggriculture-pipe16-idle-workers)
and [haodou092's self-contained package](https://www.kaggle.com/code/haodou092/notebookdb6965aa8e).
Opening wheat improvement by Dmitrii Gluzdov.

Original credits and Apache-2.0 notices are retained in the archive.
Game environment by [Kaggle](https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/kaggriculture).
