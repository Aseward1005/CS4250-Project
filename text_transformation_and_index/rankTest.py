import database_manager as database_manager
import rank as rank
import rankOrder as rankOrder

def main():
    db = database_manager.connectDatabase()

    matrix, prof, vocab = rank.rank(db.index, "soil special")

    queryWeights = rankOrder.makeQueryWeights(vocab)
    print(rankOrder.rankResults(queryWeights, matrix, prof))


if __name__ == '__main__':
    main()