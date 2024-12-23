from functools import cache
import os

# --- Part Two ---
# The staff don't really like some of the towel arrangements you came up with. To avoid an endless cycle of towel rearrangement, maybe you should just give them every possible option.
#
# Here are all of the different ways the above example's designs can be made:
#
# brwrr can be made in two different ways: b, r, wr, r or br, wr, r.
#
# bggr can only be made with b, g, g, and r.
#
# gbbr can be made 4 different ways:
#
# g, b, b, r
# g, b, br
# gb, b, r
# gb, br
# rrbgbr can be made 6 different ways:
#
# r, r, b, g, b, r
# r, r, b, g, br
# r, r, b, gb, r
# r, rb, g, b, r
# r, rb, g, br
# r, rb, gb, r
# bwurrg can only be made with bwu, r, r, and g.
#
# brgr can be made in two different ways: b, r, g, r or br, g, r.
#
# ubwu and bbrgwb are still impossible.
#
# Adding up all of the ways the towels in this example could be arranged into the desired designs yields 16 (2 + 1 + 4 + 6 + 1 + 2).
#
# They'll let you into the onsen as soon as you have the list. What do you get if you add up the number of different ways you could make each design?

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        data = file.read().strip().split('\n\n')
        patterns = set(data[0].split(', '))
        designs = data[1].split('\n')

        @cache
        def count_ways(design):
            if not design:
                return 1
            ways = 0
            for pattern in patterns:
                if design.startswith(pattern):
                    ways += count_ways(design[len(pattern):])
            return ways
        
        result = sum([count_ways(design) for design in designs])
        print(result)
