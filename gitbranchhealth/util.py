import os
from os import path

def isoDateComparator(aTupleList1, aTupleList2):
  """
  Comparison function to compare two branch tuples.

  @param aTupleList1 A branch tuple containing the following:
         1) The branch name and 2) A date tuple, with each tuple continaing the
         following: 2a) A human-readable date (e.g. '2 days ago'), and 2b) an
         iso-standardized date for comparison with other dates. Note that 2a and
         2b should be equivalent, with 2a being less accurate, but more easily
         interpretable by humans.
  @param aTupleList2 A second branch tuple, with the same specification as
         aTupleList1 which should be compared to aTupleList1.

  @returns -1, If the branch represented by aTupleList1 is older than the branch
           represented by aTupleList2; 1 if the branch represented by
           aTupleList2 is older than the branch represented by aTupleList1;
           0, otherwise.
  """
  (branchName1, valueTuple1) = aTupleList1
  (branchName2, valueTuple2) = aTupleList2

  (humanDate1, isoDate1) = valueTuple1
  (humanDate2, isoDate2) = valueTuple2

  if isoDate1 < isoDate2:
    return -1
  elif isoDate1 == isoDate2:
    return 0

  return 1
