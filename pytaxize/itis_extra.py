# def itis_downstream(tsn, downto):
#     '''
#     Retrieve all taxa names or TSNs downstream in hierarchy from given TSN.

#     :param tsn: A taxonomic serial number.
#     :param downto: The taxonomic level you want to go down to. See examples below.
#          The taxonomic level IS case sensitive, and you do have to spell it
#          correctly. See \code{data(rank_ref)} for spelling.
#     :param verbose: logical; If TRUE (default), informative messages printed.

#     Usage:
#     pytaxize.itis_downstream(tsn=846509, downto="Genus")

#     # getting families downstream from Acridoidea
#     pytaxize.itis_downstream(tsn=650497, "Family")

#     # getting species downstream from Ursus
#     pytaxize.itis_downstream(tsn=180541, downto="Species")
#     '''
#     dat = pd.read_csv("rank_ref.csv", header=False)
#     downto2 = dat[dat['ranks'].str.contains(downto)]['rankId']
#     torank_ids = dat[dat[dat['ranks'].str.contains(downto)].index : dat.shape[0]]['rankId']

#     # stuff = [x for x in dat.ranks]
#     # things = []
#     # for i in range(len(stuff)):
#     #     ss = downto in stuff[i]
#     #     things.append(ss)
#     # dat2 = dat.join(pd.DataFrame(things, columns=['match']))
#     # subset = dat2[dat2.loc[dat2.match == True].index[0]: dat2.shape[0]]
#     # torank = [x.split(',')[0] for x in subset.ranks]

#     tsn2 = convertsingle(tsn)

#     stop_ = "not"
#     notout = pd.DataFrame(columns=['rankName'])
#     out = []
#     while(stop_ == "not"):
#         temp = []
#         if(len([x for x in notout.rankName]) == 0):
#             temp = pytaxize.gettaxonomicranknamefromtsn(tsn2)
#         else:
#             temp = notout
#         tt = pytaxize.gethierarchydownfromtsn(temp['tsn'])

#         names = []
#         for i in xrange(len(tt['tsn'])):
#             d = pytaxize.gettaxonomicranknamefromtsn(tt['tsn'][i])
#             names.append(d)
#         names2 = pd.DataFrame(names)
#         tt = tt.merge(names2, on='tsn')
#         if(tt[tt['rankId'].str.contains(downto2.to_string().split(' ')[-1])].shape[0] > 0):
#             out.append(tt[tt['rankId'].str.contains(downto2.to_string().split(' ')[-1])])

#         if(tt.drop(matched.index).shape[0] > 0):
#             shit = list(set([str(x) for x in torank_ids.tolist()]) - set(tt['rankId'].tolist()))
#             notout = pd.DataFrame([tt[tt['rankId'].str.contains(x)] for x in shit])
#         else:
#             notout = pd.DataFrame([downto], columns=['rankName'])

#         if(all(notout['rankName'] == downto)):
#             stop_ = "fam"
#         else:
#             tsns = notout$tsn
#             stop_ = "not"
#     tmp = ldply(out)
#     names(tmp) = tolower(names(tmp))
#     tmp
