# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 17:33:08 2021

@author: edbin
"""

'''
Un sistema di e-cash consente agli utenti registrati di effettuare
    transazioni in valuta elettronica. Indicheremo la moneta elettronica in
    questione con il simbolo Ħ.
    Per il trasferimento di Ħ, gli utenti ricorrono ad agenti intermediari
    che gestiscono le transazioni al prezzo di una commissione. Le
    commissioni di transazione si basano su percentuali variabili, decise
    dagli intermediari.

Lo scopo di questo programma è quello di elaborare un registro delle transazioni
    tra gli utenti del sistema di e-cash che riporti:
    1) una lista con il saldo finale di ogni conto dei giocatori coinvolti;
    2) una lista con l'importo finale guadagnato da ogni intermediario;
    3) una lista in cui, per ogni intermediario, una lista annidata riporta i
       debiti residui dei conti del giocatore (0 se non è stato accumulato
       alcun debito, altrimenti un numero intero negativo).
    I risultati (1), (2) e (3) devono essere elementi di una tupla.

In particolare, deve essere progettata la seguente funzione:
     ex1 (acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log)
     dove
     - acn1, acn2 e acn3 sono i numeri di conto del giocatore 1, 2 e 3,
       rispettivamente;
     - imd_acn1 e imd_acn2 sono i numeri di conto degli intermediari 1 e 2,
       rispettivamente;
     - init_amount è l'importo iniziale nei conti dei tre giocatori
       (assumiamo che tutti i giocatori inizino con lo stesso importo iniziale);
     - i conti degli intermediari iniziano con un saldo di 0Ħ;
     - transact_log è un elenco di transazioni; ogni transazione è una tupla
       che consta dei seguenti elementi:
       · una coppia di numeri interi indicanti il numero del conto del
         mittente e il numero del conto del destinatario;
       · l'importo trasferito;
       · il numero del conto dell'intermediario;
       · la percentuale della commissione di transazione (da calcolare in
         base all'importo trasferito).

Ad esempio, la seguente tupla:
       ((0x44AE, 0x5B23), 800, 0x1612, 4)
     indica una transazione che trasferisce 800Ħ dal numero di conto 0x44AE al
     conto numero 0x5B23, con il servizio dell'intermediario che riceverà il
     4% di 800Ħ (quindi, 32Ħ) sul proprio conto a 0x1612.
     Di conseguenza,
     - il saldo del mittente (0x44AE) diminuirà di
         800 + 32 = 832Ħ,
     - il saldo del destinatario (0x5B23) aumenterà di
         800Ħ,
     - l'intermediario guadagnerà e depositerà sul proprio conto (0x1612)
         32Ħ.

Si noti che se i fondi nel conto del mittente sono insufficienti,
    la transazione viene dichiarata non valida dall'intermediario.
    L'intermediario riceverà comunque la commissione dal mittente, se ci sono
    abbastanza Ħ nel conto del mittente. Se il mittente non può pagare la
    commissione di transazione, l'intermediario riceverà tutti i fondi
    rimanenti e prenderà la sua parte dalle successive transazioni inviate al
    debitore fino al pagamento del debito. Considerando l'esempio precedente,
    se ci sono solo 700Ħ nel conto 0x44AE, l'intermediario guadagna 32Ħ e
    l'importo in 0x44AE diminuisce a 668Ħ. Se ci sono solo 10Ħ nel conto
    0x44AE, l'intermediario guadagna 10Ħ e l'importo in 0x44AE diminuisce a
    0Ħ; inoltre, l'intermediario mantiene un credito di 22Ħ con il mittente. Il
    mittente sarà obbligato a rimborsare i 22Ħ ottenendo l'importo dovuto
    dalle transazioni ricevute successivamente fino all'estinzione del debito.

    Se si accumula un debito nei confronti di due intermediari, i fondi vanno
    per primo all'intermediario che ha il credito più elevato e il resto va
    all'altro intermediario. Ad esempio, se il giocatore 1 deve 300Ħ
    all'intermediario 1 e 200Ħ all'intermediario 2, quando il giocatore 1
    riceve 400Ħ, 300Ħ vengono pagati all'intermediario 1 e 100Ħ vengono
    pagati all'intermediario 2. Se lo stesso importo è dovuto a entrambi gli
    intermediari, il rimborso è equamente diviso. Ad esempio, il giocatore 2
    deve 100Ħ all'intermediario 1 e 100Ħ all'intermediario 2; quando il
    giocatore 2 riceve 100Ħ, 50Ħ vanno a ciascun intermediario.

Ad esempio,
    ex1(0x5B23, 0xC78D, 0x44AE, 0x1612, 0x90FF, 1000,
        [ ((0x44AE, 0x5B23),  800, 0x1612,  4),
          ((0x44AE, 0xC78D),  800, 0x90FF, 10),
          ((0xC78D, 0x5B23),  400, 0x1612,  8),
          ((0x44AE, 0xC78D), 1800, 0x90FF, 12),
          ((0x5B23, 0x44AE),  100, 0x1612,  2)]
    ritorna
    ( [2098, 568, 0], [66, 268], [ [0, 0, 0], [0, 0, -28] ] )
    perché tutti gli utenti iniziano con 1000Ħ nei loro conti ed, al termine,
    – il saldo dell’utente 1 ammonta a 2098Ħ,
    – il saldo dell’utente 2 ammonta a 568Ħ,
    – il saldo dell’utente 3 ammonta a 0Ħ,
    – l'intermediario 1 ha guadagnato 66Ħ,
    – l'intermediario 2 ha guadagnato 268Ħ,
    – l’utente 3 rimane in debito di 28Ħ con l'intermediario 2.

Il TIMEOUT per ciascun test è di 0.5 secondi

ATTENZIONE: è proibito:
    - importare altre librerie
    - usare variabili globali  transact_log[x][1] --> transaction[1]
    - aprire file
'''
def ex1(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log):
    output = ()
    saldo_giocatore = {}
    saldo_giocatore[acn1] = init_amount
    saldo_giocatore[acn2] = init_amount
    saldo_giocatore[acn3] = init_amount              
    guadagno_intermediario = {}                       
    guadagno_intermediario[imd_acn1] = 0
    guadagno_intermediario[imd_acn2] = 0    
    debiti = {}
    debiti[(acn1, imd_acn1)] = 0
    debiti[(acn1, imd_acn2)] = 0
    debiti[(acn2, imd_acn1)] = 0
    debiti[(acn2, imd_acn2)] = 0
    debiti[(acn3, imd_acn1)] = 0
    debiti[(acn3, imd_acn2)] = 0    
    for trans in transact_log:
        importo = trans[1]
        if importo == 0:
            continue
        per = round((importo*trans[3])/100)
        mittente, ricevente, intermediario = trans[0][0], trans[0][1], trans[2]
        if importo+per > saldo_giocatore[mittente]:
        #se l'importo+per è maggiore dei soldi del mittente
            if saldo_giocatore[mittente] - per < 0:
            #se il mittente tolta la percentuale va in debito
                debito = saldo_giocatore[mittente] - per    
                #salvo il debito (calcolato sottraendo al mittente la percetuale) in una variabile
                guadagno_intermediario[intermediario] += saldo_giocatore[mittente]
                #aggiungo all'agente i soldi rimaneti nel conto del mittente
                debiti[(mittente, intermediario)] += debito
                #aggiungo al dizionario il debito del mittente con l'agente
                saldo_giocatore[mittente] = 0
                #porto a 0 il conto del mittente
            else:          
            #se il mittente non va in debito
                guadagno_intermediario[intermediario] += per
                #do all'agente la percetuale
                saldo_giocatore[mittente] -= per
                #tolgo al mittente la percentuale           
        else:
        #se l'importo è minore o uguale al conto del mittente
            saldo_giocatore[mittente] -= importo + per
            guadagno_intermediario[intermediario] += per
            if debiti[(ricevente, imd_acn1)] != 0 and debiti[(ricevente, imd_acn2)] == 0:
            # se il ricevente è indebitato con l'agente1 e non con l'agente2
                debiti[(ricevente, imd_acn1)] += importo
                #aggiungo al debito l'importo
                if debiti[(ricevente, imd_acn1)] <= 0:
                #se il debito è minore o uguale a 0 (non è stato ripagato a pieno o i soldi sono precisi)
                    guadagno_intermediario[imd_acn1] += importo
                    #aggiungo all'agente l'importo
                else:
                #se il debito è stato ripagato troppo
                    saldo_giocatore[ricevente] += debiti[(ricevente, imd_acn1)]
                    #aggiungo al ricevente i soldi avanzati dal pagamento del dibito
                    guadagno_intermediario[imd_acn1] += abs(debiti[(ricevente, imd_acn1)] - importo)
                    #aggiungo i soldi pagati del debito1 all'agente1
                    debiti[(ricevente, imd_acn1)] = 0
                    #porto a 0 il debito con l'agente1
            elif debiti[(ricevente, imd_acn2)] != 0 and debiti[(ricevente, imd_acn1)] == 0:
            # se il ricevente è indebitato con l'agente2 e non con l'agente 2
                debiti[(ricevente, imd_acn2)] += importo
                #aggiungo al debito l'importo
                if debiti[(ricevente, imd_acn2)] <= 0:
                #se il debito è minore o uguale a 0 (non pagato abbastanza o pagato preciso)
                    guadagno_intermediario[imd_acn2] += importo
                    #aggiungo all'agente2 i soldi del debito
                else:
                #se il debito è stato ripagato troppo
                    saldo_giocatore[ricevente] += debiti[(ricevente, imd_acn2)]
                    #do al ricevente i soldi in più
                    guadagno_intermediario[imd_acn2] += abs(debiti[(ricevente, imd_acn2)] - importo)    
                    #aggiungo i soldi pagati del debito2 all'agente2
                    debiti[(ricevente, imd_acn2)] = 0
                    #porto a 0 i debiti del ricevente con l'agente 2                    
            elif debiti[(ricevente, imd_acn1)] and debiti[(ricevente, imd_acn2)] != 0:
            #se il ricevente è indebitato con entrambi gli agenti
                if debiti[(ricevente, imd_acn1)] < debiti[(ricevente, imd_acn2)]:
                    #se il debito1 è < (più grande) del debito2
                    debiti[(ricevente, imd_acn1)] += importo
                    #aggiugno al debtio1 l'importo
                    if debiti[(ricevente, imd_acn1)] <= 0:                                       
                      #se il debito1 è non e stato ripagato a pieno o precisamente
                      guadagno_intermediario[imd_acn1] += importo
                      #aggiungo i soldi all'agente1
                    else:
                    #se il debito è stato ripagato troppo    
                        guadagno_intermediario[imd_acn1] += abs(debiti[(ricevente, imd_acn1)] - importo)
                        #aggiungo i soldi pagati del debito1 all'agente1
                        troppi = debiti[(ricevente, imd_acn1)] 
                        #salvo in una variabile i soldi pagati in più all'agente 1
                        debiti[(ricevente, imd_acn2)] += troppi
                        #aggiungo al debito2 i soldi in più                       
                        debiti[(ricevente, imd_acn1)] = 0
                        #porto a 0 il debito1
                        if debiti[(ricevente, imd_acn2)] <= 0:
                            #se il debito2 non e stato ripagato a pieno o precisamente
                            guadagno_intermediario[imd_acn2] += troppi
                            #aggiungo all'agente2 i soldi in più dati dall'agente1
                        else:
                            #se il debito è stato pagato troppo
                            guadagno_intermediario[imd_acn2] +=  abs(troppi - debiti[(ricevente, imd_acn2)])
                            #do all'agente2 i soldi in più dell'agente1
                            saldo_giocatore[ricevente] += debiti[(ricevente, imd_acn2)]
                            #aggiungo i soldi in più al ricevente
                            debiti[(ricevente, imd_acn2)] = 0
                            #porto il debito2 a 0                             
                elif debiti[(ricevente, imd_acn1)] > debiti[(ricevente, imd_acn2)]:
                #se il debito1 è < (più grande) del debito2
                    debiti[(ricevente, imd_acn2)] += importo
                    #aggiugno al debito1 l'importo
                    if debiti[(ricevente, imd_acn2)] <= 0:                                       
                      #se il debito1 è non e stato ripagato a pieno o precisamente
                      guadagno_intermediario[imd_acn2] += importo
                      #aggiungo i soldi all'agente1
                    else:
                    #se il debito è stato ripagato troppo    
                        guadagno_intermediario[imd_acn2] += abs(debiti[(ricevente, imd_acn2)] - importo)
                        #aggiungo i soldi pagati del debito1 all'agente1
                        troppi = debiti[(ricevente, imd_acn2)] 
                        #salvo in una variabile i soldi pagati in più all'agente 1
                        debiti[(ricevente, imd_acn1)] += troppi
                        #aggiungo al debito2 i soldi in più                       
                        debiti[(ricevente, imd_acn2)] = 0
                        #porto a 0 il debito1
                        if debiti[(ricevente, imd_acn1)] <= 0:
                            #se il debito2 non e stato ripagato a pieno o precisamente
                            guadagno_intermediario[imd_acn1] += troppi
                            #aggiungo all'agente2 i soldi in più dati dall'agente1
                        else:
                            #se il debito è stato pagato troppo
                            guadagno_intermediario[imd_acn1] +=  abs(troppi - debiti[(ricevente, imd_acn1)])
                            #do all'agente2 i soldi in più dell'agente1
                            saldo_giocatore[ricevente] += debiti[(ricevente, imd_acn1)]
                            #aggiungo i soldi in più al ricevente
                            debiti[(ricevente, imd_acn1)] = 0
                            #porto il debito2 a 0                                                           
                elif debiti[(ricevente, imd_acn1)] == debiti[(ricevente, imd_acn2)]:
                #se il ricevente è ugualemente indebitato con entrambi gli agenti
                    debiti[(ricevente, imd_acn1)] += importo/2
                    #aggiungo metà dell'importo all'agente1
                    debiti[(ricevente, imd_acn2)] += importo/2
                    #aggiungo metà dell'importo all'agente2
                    if debiti[(ricevente, imd_acn1)] and debiti[(ricevente, imd_acn2)] <= 0:
                        #se entrambi i debiti non sono stati ripagati pienamente o precisamente
                        guadagno_intermediario[imd_acn1] += round(importo/2)
                        #aggiungo i soldi all'agente1
                        guadagno_intermediario[imd_acn2] += round(importo/2)
                        #aggiungo i soldi all'agente2                        
                    elif debiti[(ricevente, imd_acn1)] > 0 and debiti[(ricevente, imd_acn2)] <= 0:
                    #se il debito1 è stato pagato troppo e il debito 2 non pienamente o precisamente
                        guadagno_intermediario[imd_acn1] = abs(debiti[(ricevente, imd_acn1)] - importo/2)
                        #aggiungo all'agente1 i soldi del debito
                        troppi = debiti[(ricevente, imd_acn1)] 
                        debiti[(ricevente, imd_acn2)] += debiti[(ricevente, imd_acn1)]
                        #aggiungo il debito1 al debito2
                        debiti[(ricevente, imd_acn1)] = 0
                        #porto a 0 il debito1
                        if debiti[(ricevente, imd_acn2)] <= 0:
                        #se il debito2 è stato pagato  non pienamente o precisamente
                            guadagno_intermediario[imd_acn2] += troppi
                        else:
                        #se è stato pagato troppo
                            guadagno_intermediario[imd_acn2] +=  abs(troppi - debiti[(ricevente, imd_acn2)])
                            #do all'agente2 i soldi in più dell'agente1
                            saldo_giocatore[ricevente] += debiti[(ricevente, imd_acn2)]
                            #aggiungo al ricevente i soldi in più
                            debiti[(ricevente, imd_acn2)] = 0
                            #porto a 0 il debito2                            
                    elif debiti[(ricevente, imd_acn1)] <= 0 and debiti[(ricevente, imd_acn2)] > 0:
                    #se il debito1 è stato pagato troppo e il debito 2 non pienamente o precisamente
                        guadagno_intermediario[imd_acn2] = abs(debiti[(ricevente, imd_acn2)] - importo/2)
                        #aggiungo all'agente1 i soldi del debito
                        troppi = debiti[(ricevente, imd_acn2)] 
                        debiti[(ricevente, imd_acn1)] += debiti[(ricevente, imd_acn2)]
                        #aggiungo il debito1 al debito2
                        debiti[(ricevente, imd_acn2)] = 0
                        #porto a 0 il debito1
                        if debiti[(ricevente, imd_acn1)] <= 0:
                        #se il debito2 è stato pagato  non pienamente o precisamente
                            guadagno_intermediario[imd_acn1] += troppi
                        else:
                        #se è stato pagato troppo
                            guadagno_intermediario[imd_acn1] +=  abs(troppi - debiti[(ricevente, imd_acn1)])
                            #do all'agente2 i soldi in più dell'agente1
                            saldo_giocatore[ricevente] += debiti[(ricevente, imd_acn1)]
                            #aggiungo al ricevente i soldi in più
                            debiti[(ricevente, imd_acn1)] = 0
                            #porto a 0 il debito2                            
                    elif debiti[(ricevente, imd_acn1)] > 0 and debiti[(ricevente, imd_acn2)] > 0:
                    #se sono stati pagati troppo entrambi i debiti
                          guadagno_intermediario[imd_acn1] = abs(debiti[(ricevente, imd_acn1)] - importo/2)
                          #do all'agente1 i soldi del debito
                          guadagno_intermediario[imd_acn2] = abs(debiti[(ricevente, imd_acn2)] - importo/2)
                          #do all'agente2 i soldi del debito
                          saldo_giocatore[ricevente] += debiti[(ricevente, imd_acn1)] + debiti[(ricevente, imd_acn2)]
                          #aggiungo al ricevente i soldi in più sia del debito1 che del debito2
                          debiti[(ricevente, imd_acn1)] = 0
                          #porto a 0 il debito1
                          debiti[(ricevente, imd_acn2)] = 0
                          #porto a 0 il debito2
            else:
            #se il ricevente non ha buffi con l'agente
                saldo_giocatore[ricevente] += importo
                #aggiungo al ricevente i soldi dell'importo
    output = ( [saldo_giocatore[acn1], saldo_giocatore[acn2], saldo_giocatore[acn3]], [guadagno_intermediario[imd_acn1], guadagno_intermediario[imd_acn2]], [ [debiti[(acn1, imd_acn1)], debiti[(acn2, imd_acn1)], debiti[(acn3, imd_acn1)]], [debiti[(acn1, imd_acn2)], debiti[(acn2, imd_acn2)], debiti[(acn3, imd_acn2)]] ] )
    return output 


