class Stitch:
    def __init__(self, name: str, count: int = 1, consumes: int = 1, creates: int = 1) -> None:
        '''
        Initializes a stitch object.
        
        Parameters:
        -----------
        name: str
            The shorthand name of the stitch.
        count: int
            The number of times the stitch is repeated.
        consumes: int
            The number of stitches in the previous row/round consumed by this stitch.
        creates: int
            The number of stitches created by this stitch for the next row/round.
        '''
        self.name = name
        self.count = count
        self.consumes = consumes
        self.creates = creates

    def __mul__(self, other) -> 'Stitch':
        if not isinstance(other, int):
            raise TypeError('Cannot multiply stitch by non-int')
        elif other <= 0:
            raise ValueError('Cannot multiply stitch by non-positive integer')
        return Stitch(self.name, self.count * other, self.consumes * other, self.creates * other)

    __rmul__ = __mul__

    def __str__(self) -> str:
        return f'{self.name}{self.count}'

    def __add__(self, other) -> 'Pattern':
        if not isinstance(other, Stitch):
            raise TypeError('Cannot add non-stitch to stitch')

        return Pattern([self, other])


class Pattern:
    def __init__(self, patterns: list = [], count: int = 1) -> None:
        self.patterns = patterns
        self.count = count

    @property
    def consumes(self) -> int:
        return sum(pattern.consumes for pattern in self.patterns) * self.count

    @property
    def creates(self) -> int:
        return sum(pattern.creates for pattern in self.patterns) * self.count

    def __add__(self, other) -> 'Pattern':
        if not isinstance(other, Stitch) and not isinstance(other, Pattern):
            raise TypeError('Cannot add non-stitch to pattern')
        
        if isinstance(other, Stitch):
            if self.count == 1:
                return Pattern(self.patterns + [other])
            return Pattern([self, other])
        
        if isinstance(other, Pattern):
            if self.count == other.count == 1:
                return Pattern(self.patterns + other.patterns)
            elif self.count == 1:
                return Pattern(self.patterns + [other])
            elif other.count == 1:
                return Pattern([self] + other.patterns)
        return Pattern([self, other])

    def __mul__(self, other) -> 'Pattern':
        if not isinstance(other, int):
            raise TypeError('Cannot multiply pattern by non-int')
        elif other <= 0:
            raise ValueError('Cannot multiply pattern by non-positive integer')
        return Pattern(self.patterns, self.count * other)

    __rmul__ = __mul__

    def __str__(self) -> str:
        pattern_str = ', '.join(str(pattern) for pattern in self.patterns)
        if self.count > 1:
            return f'[{pattern_str}] * {self.count}'
        return pattern_str
    