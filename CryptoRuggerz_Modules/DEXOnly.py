from pycoingecko import CoinGeckoAPI
from pprint import pprint
from simple_colors import *
import colorama
from colorama import Fore
cg = CoinGeckoAPI()

global DEXSCORE

print(Fore.LIGHTGREEN_EX + "\n============ STARTING DECENTRALSED EXCHANGE CHECK ============\n" + Fore.RESET)

#list of Exchanges coin being analyze is listed on
listOfExchangesCoinIsOn = []
marketScore = []
#list of good reputable exchanges
listOfGoodCEX =["Binance", "Coinbase Exchange", "Huobi Global", "KuCoin", "Crypto.com Exchange", "Gate.io", "FTX", "Binance US", "Kraken", "Bitfinex","Gemini","Bittrex","Poloniex","OKEx","Bithumb"]
#list of de centralised (DEX) exchanges
listOfDEX=["PancakeSwap (v2)","Uniswap (v3)","Uniswap (v2)","Sushiswap","Trader Joe","Raydium","Curve Finance","Orca","Compound Finance","Mdex","Spookyswap","Ref Finance","Mdex BSC",
"Shibaswap","Quickswap","Sushiswap (Polygon POS)","Bancor Network","Serum DEX","JustSwap","Loopring AMM","Uniswap (Arbitrum One)","Balancer (v2)","Dodo (Polygon)","Terraswap","Pangolin",
"Tokenlon","Osmosis","DODO","SpiritSwap","Uniswap (Optimism)","Sushiswap (Arbitrum One)","Defi Kingdoms","Dodo BSC","Kwenta","Solarbeam","Balancer (v1)","SecretSwap","ApeSwap (Polygon)",
"Dfyn","CherrySwap","Balancer (Polygon)","Sushiswap (Harmony)","Binance DEX","Loopring","WaultSwap","DMM (BSC)","Polkaswap","Swop.Fi","Balanced Network","Sushiswap Celo","Balancer (Arbitrum)",
"Quipuswap","ZilSwap","DMM (Ethereum)","Deversifi","DMM (Avalanche)","DeFi Swap","DMM (Polygon)","Kaidex","Sushiswap (BSC)","StellarTerm","Acsi Finance","WaultSwap Polygon","ViperSwap","Kava Swap",
"1inch Liquidity Protocol","Dodo (Arbitrum)","ZKSwap (v2)","Clipper (Ethereum)","Kuswap","ViteX","Paintswap","0x Protocol","Ubeswap","Mimo","Binance DEX (Mini)","Unicly","Bisq","Sushiswap (xDai)",
"Swapr (Arbitrum)","Nash","Pancakeswap (Others)","ComethSwap","Swapr","Honeyswap","Luaswap","Baguette","Sushiswap (Fantom)","PoloniDEX","TronTrade","Aave","Newdex","Demex","Kyber Network","TokenSets",
"vSwap BSC","Cybex DEX","Honeyswap (Polygon)","Nexus Mutual","PolyZap","Levinswap (xDai)","ZKSwap (v1)","SakeSwap","Polyient Dex","Idex","PinkSwap","Sashimiswap","dex.blue","TomoDEX","BepSwap","Everbloom",
"Uniswap (v1)","PantherSwap","DDEX","Bamboo Relay","Bitcratic","Anyswap","PancakeSwap (v1)","Orderbook.io","Dolomite","BurgerSwap","ForkDelta","ApeSwap","1inch Liquidity Protocol (BSC)","Joyso","Radar Relay",
"Neblidex","Ethex","BSCswap","Saturn Network","Mooniswap","1inch","Bakeryswap","Value Liquid","Julswap","Allbit","Swapr (Ethereum)","Blockonix","Zero Exchange","Niftex","OasisDEX","dYdX","Switcheo",
"Beethoven X","Sifchain"]

#flag for if coin is not listed on any reputable exchanges
flag =0
#track number of centralised exchange the coin is on
cexpoint =0
#track number of DEX exchange the coin is on
dexpoint =0

DEXstart = True
DEXtryflag =1
while(DEXstart):
    try:
        if DEXtryflag ==1:
            coinID = input("Please Enter Coin id OR enter SKIP to skip DEX only analysis: ")
            if coinID == "SKIP":
                DEXtryflag = 0
                break
            #API call to get info about the coin
            allinfo = cg.get_coin_ticker_by_id(coinID) 
            break
    except Exception:
        print("Coin doesnt exist in database or wrong spelling")
        continue
    break

if DEXtryflag != 0:
    #access the dictionary to get more specifc info about the coin
    allexchangesinfo = allinfo["tickers"]

    #loop through list to get the exchanges the coin is listed on
    i=0
    for x in allexchangesinfo:
        eachExchangeInfo = allexchangesinfo[i]
        market = eachExchangeInfo["market"]
        marketname = market["name"]
        listOfExchangesCoinIsOn.append(marketname)
        i+=1

    #remove duplicates
    listOfExchangesCoinIsOn = list(dict.fromkeys(listOfExchangesCoinIsOn))

    '''
    #loop through list to get the exchanges rating based on coingecko's scoring
    a=0
    for x in allexchangesinfo:
        eachExchangeInfo = allexchangesinfo[a]
        market = eachExchangeInfo["trust_score"]
        marketScore.append(market)
        a+=1
    '''
    print("\nGreen have a high probability is safe.")
    print("Yellows means proceed with caution.")
    print("Reds are unsafe.")
    print("Blues are okayish however might turn yellow to red.\n")

    print("Reputable/ Popular CEX Exchange listed")
    #loop to check if the coin is listed on reputable CEXs
    for x in listOfGoodCEX:
        for y in listOfExchangesCoinIsOn:
            if y == x:
                flag =1
                cexpoint += 1
                print(green(y, 'bold'))
                listOfExchangesCoinIsOn.remove(y)

    #loop to check if the coin is listed on DEXs
    print("\nDEX Exchange listed")
    for a in listOfDEX:
        for b in listOfExchangesCoinIsOn:
            if b == a:
                if flag == 0:
                    dexpoint +=1
                    print(red(b, 'bold'))
                    listOfExchangesCoinIsOn.remove(b)
                else:
                    dexpoint +=1
                    print(yellow(b, 'bold'))
                    listOfExchangesCoinIsOn.remove(b)

    print("\nOther CEX Exchange listed")
    #loop to print remaining CEXs
    for c in listOfExchangesCoinIsOn:
        if flag == 0:
            print(yellow(c, 'bold'))
        else:
            print(blue(c, 'bold'))
        


    #rating is based on the number of good exchanges coin is listed on
    rating = (cexpoint/len(listOfGoodCEX)) *100
    DEXSCORE = (rating / 100) * 0.1
    #pprint(marketScore)
    print("\nCoin " + coinID + " rating is : " + str(rating) + " out of 100")
    print("Number of reputable CEX exchange listed is " + str(cexpoint) + " out of " + str(len(listOfGoodCEX)))
    print("Number of DEX exchange listed is " + str(dexpoint) + " out of " + str(len(listOfDEX)))
    DEXstart = False
    DEXtryflag = 0
    print(Fore.RED + "\n============ END OF DECENTRALISED EXCHANGE LISTING CHECK ============\n" + Fore.RESET)

else:
    print(Fore.RED + "\n============ DECENTRALISED EXCHANGE LISTING CHECK SKIPPED! ============\n" + Fore.RESET)


