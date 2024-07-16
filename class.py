import os.path
import sheetsbase

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
spreadsheet_ID = "1VidXQeKAelgcGtEf7bkFqQX7VB82ATwCX8ok4mcIqpM"

# no need to redo code :)
def main():
  sheetsbase.main()
  result = (
      sheetsbase.getSheet().values()
      .get(spreadsheetId=spreadsheet_ID,range="A:A")
      .execute()
  )
  global names
  names = result.get("values", [])
  names.pop(0) # or we can just not include "Person" in the range

# This function splits names into separate strings.
def splitComma(input): 
  if input == None or input == []:
     return []
  arr = input[0][0].split(",")
  if len(arr) == 1 or len(arr) == 0:
    return arr
  newArr = []
  for elt in arr:
    newArr.append(elt.strip())
  return newArr

# return the row number of the name
def searchName(name):
    global names
    global counter
    counter = 0
    name.strip()
    out = binarySearch(names, 0, len(names) - 1, name)
    return out      
# binary search!
def binarySearch(values, lo, hi, target):
    if hi >= lo:
      global counter
      counter = counter + 1
      if counter > 20:
        exit()
      mid = (hi + lo) // 2
      # print("mid: " + str(mid) + " and its " + values[mid][0])
      # print("target: " + target)
      temp = values[mid][0].strip()
      if(temp == target):
        return mid
      match temp == target: 
          case False:
              if target > temp: # search right
                  # print("goin right: " + str(mid + 1) + " to " + str(hi) + " and its from " + values[mid+1][0] + " to " + values[hi][0])
                  return binarySearch(values, mid + 1, hi, target)
              if target < temp: # search left
                  # print("going left: " + str(lo) + " to " + str(mid - 1) + " and its from " + values[lo][0] + " to " + values[mid - 1][0])
                  return binarySearch(values, lo, mid - 1, target)
          case True:
              return mid
          case _:
              print('binarySearch: Not found womp womp')
              return
    else: 
       return -3 # nada

class Tree:
  def __init__(self, input):
    self.root = input
    self.check = []
    self.dict = {}
  def helpFunction(self):
    makeTree(self.check, self.dict, self.root)
  

def makeTree(arr, newTree, input):
  arr.append(input)
  print("findFam: " + input)
  if input == None or input == []:
     return 
  newTree[input] = {}
  newTree[input]["row"] = searchName(input) + 2
  newTree[input]["bigs"] = splitComma(sheetsbase.getData(spreadsheet_ID, "C" + str(newTree[input]["row"])))
  newTree[input]["littles"] = splitComma(sheetsbase.getData(spreadsheet_ID, "B" + str(newTree[input]["row"])))
  for bigName in newTree[input]["bigs"]:
    if(bigName not in arr):
      makeTree(arr, newTree, bigName)
  for lilName in newTree[input]["littles"]:
    if(lilName not in arr):
      makeTree(arr, newTree, lilName)

  



if __name__ == "__main__":
   main()

# test code :)
tree = Tree("Joshua Sixto Beltran")

tree.helpFunction()
print(tree.dict)
