import json


class VoteCounter():

    def __init__(self):
        self.votes = []
        self.last_vote = 0
        self.calculated = False

    def add_vote(self, vote):
        '''
        Adds a vote to the vote counter. If a vote for the same move already
        exists, increments the number of votes for that move
        :param vote: JSON object representing a vote
        :return:
        '''
        vote = json.loads(vote)
        self.calculated = False

        # find existing vote and increment counter
        for v in self.votes:
            if v[1] == vote:
                v[0] += 1
                return

        # if no votes were found, add a vote
        self.votes.append([1, vote])

    def calculate_votes(self):
        '''
        Calculates which votes are the most popular
        :return:
        '''
        self.votes.sort(key=lambda v: -v[0])
        self.calculated = True
        self.last_vote = 0

    def get_next_popular_vote(self):
        '''
        Gets the next most popular vote. Calculates the votes if needed
        :return:
        '''
        if not self.calculated:
            self.calculate_votes()

        res = None
        if self.last_vote < len(self.votes):
            res = self.votes[self.last_vote][1]
            self.last_vote += 1

        return res

    def reset(self):
        '''
        Resets the vote counter
        :return:
        '''
        self.votes = []
        self.last_vote = 0
        self.calculated = False