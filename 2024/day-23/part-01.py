import os
import polars as pl

# --- Day 23: LAN Party ---
# As The Historians wander around a secure area at Easter Bunny HQ, you come across posters for a LAN party scheduled for today! Maybe you can find it; you connect to a nearby datalink port and download a map of the local network (your puzzle input).
#
# The network map provides a list of every connection between two computers. For example:
#
# kh-tc
# qp-kh
# de-cg
# ka-co
# yn-aq
# qp-ub
# cg-tb
# vc-aq
# tb-ka
# wh-tc
# yn-cg
# kh-ub
# ta-co
# de-co
# tc-td
# tb-wq
# wh-td
# ta-ka
# td-qp
# aq-cg
# wq-ub
# ub-vc
# de-ta
# wq-aq
# wq-vc
# wh-yn
# ka-de
# kh-ta
# co-tc
# wh-qp
# tb-vc
# td-yn
# Each line of text in the network map represents a single connection; the line kh-tc represents a connection between the computer named kh and the computer named tc. Connections aren't directional; tc-kh would mean exactly the same thing.
#
# LAN parties typically involve multiplayer games, so maybe you can locate it by finding groups of connected computers. Start by looking for sets of three computers where each computer in the set is connected to the other two computers.
#
# In this example, there are 12 such sets of three inter-connected computers:
#
# aq,cg,yn
# aq,vc,wq
# co,de,ka
# co,de,ta
# co,ka,ta
# de,ka,ta
# kh,qp,ub
# qp,td,wh
# tb,vc,wq
# tc,td,wh
# td,wh,yn
# ub,vc,wq
# If the Chief Historian is here, and he's at the LAN party, it would be best to know that right away. You're pretty sure his computer's name starts with t, so consider only sets of three computers where at least one computer's name starts with t. That narrows the list down to 7 sets of three inter-connected computers:
#
# co,de,ta
# co,ka,ta
# de,ka,ta
# qp,td,wh
# tb,vc,wq
# tc,td,wh
# td,wh,yn
# Find all the sets of three inter-connected computers. How many contain at least one computer with a name that starts with t?
pl.Config(tbl_rows=-1)
if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        data = [line.strip().split('-') for line in file]
        data = pl.DataFrame(data).transpose().rename({'column_0': 'from', 'column_1': 'to'})
        links = pl.concat([
            data,
            data.select(['to', 'from']).rename({'to': 'from', 'from': 'to'})
        ])
        
        sets = links\
            .join_where(
                links,
                [
                    (pl.col('to') == pl.col('from_right')) & (pl.col('from') != pl.col('to_right')),
                ],
            )\
            .rename({
                'from': 'first',
                'to': 'second',
                'to_right': 'third',
            })\
            .join_where(
                links,
                (pl.col('third') == pl.col('from')) & (pl.col('to') == pl.col('first')),
            )\
            .filter(
                (pl.col('first') < pl.col('second')) & (pl.col('second') < pl.col('third')) &
                (pl.col('first').str.starts_with('t') | pl.col('second').str.starts_with('t') | pl.col('third').str.starts_with('t'))
            )

        print(sets.shape[0])