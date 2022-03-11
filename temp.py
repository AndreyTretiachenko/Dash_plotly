""""" try:
     with open("history.csv", "w") as f:
         f.write(r.text)
         f.close()
 except FileExistsError:
     print("File is already created")
 df = pd.read_csv("history.csv", header=None)
"""""