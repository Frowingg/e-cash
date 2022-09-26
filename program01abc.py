# -*- coding: utf-8 -*-
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
          ((0x5B23, 0x44AE),  100, 0x1612,  2)
        ]
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
    - usare variabili globali
    - aprire file
'''
def ex1(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log):
    output = ()
    reg =  {acn1 : int(init_amount), acn2 : int(init_amount) , acn3 : int(init_amount), 
            imd_acn1 : 0 , imd_acn2 : 0,
            'debiti_'+ str(imd_acn1) + '_' + str(acn1) : 0, 'debiti_'+ str(imd_acn1) + '_' + str(acn2) : 0,
            'debiti_'+ str(imd_acn1) + '_' + str(acn3) : 0,
            'debiti_'+ str(imd_acn2) + '_' + str(acn1) : 0, 'debiti_'+ str(imd_acn2) + '_' + str(acn2) : 0,
            'debiti_'+ str(imd_acn2) + '_' + str(acn3) : 0}
    for x in range(len(transact_log)):
    #con un for mi scorro tutto transact_log
        importo = transact_log[x][1]
        # salvo in una variavile l'importo
        per = int((importo*transact_log[x][3])/100)
        #salvo in una variabile la percentuale
        # soldi_1 = reg[transact_log[x][0][0][0]]
        # soldi_2 = reg[transact_log[x][0][0][1]]
        # ag = reg[transact_log[x][0][2]]
        if importo == 0:
        #se l'importo è 0 passo
            pass
        elif importo > reg[transact_log[x][0][0]]:
        #se l'importo è maggiore dei soldi del mittente
            if (reg[transact_log[x][0][0]] - per) < 0:
            #se il mittente tolta la percentuale va in debito
               debito = reg[transact_log[x][0][0]] - per    
               #salvo il debito (calcolato sottraendo al mittente la percetuale) in una variabile
               reg[transact_log[x][2]] += reg[transact_log[x][0][0]]
               #aggiungo all'agente i soldi rimaneti nel conto del mittente
               reg['debiti_'+ str(transact_log[x][2]) + '_' + str(transact_log[x][0][0])] += debito
               #aggiungo al dizionario il debito del mittente con l'agente
               reg[transact_log[x][0][0]] = 0
               #porto a 0 il conto del mittente
            else:
            #se il mittente non va in debito
                reg[transact_log[x][2]] += per
                #do all'agente la percetuale
                reg[transact_log[x][0][0]] -= per
                #tolgo al mittente la percentuale
        elif importo <= reg[transact_log[x][0][0]]:
        #se l'importo è minore o uguale al conto del mittente
            reg[transact_log[x][0][0]] -= (importo + per)
            #tolgo al mittente l'importo + la percetuale
            if reg[transact_log[x][0][0]] < 0:
            #se il mittente tolta la percentuale va in debito
               debito = reg[transact_log[x][0][0]]
               #salvo il debito in una variabile
               reg[transact_log[x][2]] += reg[transact_log[x][0][0]] + per 
               #aggiungo all'agente i soldi rimaneti nel conto del mittente
               reg['debiti_'+ str(transact_log[x][2]) + '_' + str(transact_log[x][0][0])] += debito
               #aggiungo al dizionario il debito del mittente con l'agente
               reg[transact_log[x][0][0]] = 0
               #porto a 0 il conto del mittente
            else:
            #se il mittente non va in debito
                reg[transact_log[x][2]] += per
                #aggiungo all'agente la percetuale  
            if reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] != 0:
            # se il ricevente è indebitato con l'agente
                reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] += importo
                if reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] >= 0:
                    reg[transact_log[x][0][1]] += reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])]
                    reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] = 0
                else:
                    pass
            elif reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] != 0:
            # se il ricevente è indebitato con l'agente
                reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] += importo
                if reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] >= 0:
                    reg[transact_log[x][0][1]] += reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])]
                    reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] = 0
                else:
                    pass
            elif reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] and reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] != 0:
                if reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] < reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])]:
                    reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] += importo
                    if reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] >= 0:
                        reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] += reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])]
                        reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] = 0
                        if reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] >= 0:
                            reg[transact_log[x][0][1]] += reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])]
                            reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])]
                        else:
                            pass
                    else:
                        pass
                elif reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] > reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])]:
                    reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] += importo
                    if reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] >= 0:
                        reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] += reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])]
                        reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] = 0
                        if reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] >= 0:
                            reg[transact_log[x][0][1]] += reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])]
                            reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])]
                        else:
                            pass
                    else:
                        pass
                elif reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] == reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])]:
                    reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] += importo/2
                    reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] += importo/2
                    if reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] > 0:
                        reg[transact_log[x][0][1]] += reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])]
                        reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] = 0 
                    if reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] > 0:
                        reg[transact_log[x][0][1]] += reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])]
                        reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] = 0                     
            else:
            #se il ricevento non ha buffi con l'agente
                reg[transact_log[x][0][1]] += importo
                #aggiungo al ricevente i soldi dell'importo

    output =  ([reg[acn1], reg[acn2], reg[acn3]],[reg[imd_acn1], reg[imd_acn2]],[[reg['debiti_'+ str(imd_acn1) + '_' + str(acn1)],reg['debiti_'+ str(imd_acn1) + '_' + str(acn2)],reg['debiti_'+ str(imd_acn1) + '_' + str(acn3)]],[ reg['debiti_'+ str(imd_acn2) + '_' + str(acn1)], reg['debiti_'+ str(imd_acn2) + '_' + str(acn2)], reg['debiti_'+ str(imd_acn2) + '_' + str(acn3)]]])
    print(output)
ex1(2694, 2027, 5775, 76, 242, 1000, [[[2694, 5775], 0, 242, 17], [[2027, 5775], 900, 76, 18], [[5775, 2694], 600, 76, 13], [[2027, 5775], 1100, 242, 20], [[2694, 5775], 700, 76, 4], [[2027, 5775], 1400, 76, 3], [[2694, 5775], 1000, 76, 19], [[2027, 2694], 500, 242, 17], [[5775, 2694], 1900, 76, 7], [[2027, 2694], 2800, 242, 11]])
'''
def ex1(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log):
    output = ()
    reg =  {acn1 : int(init_amount), acn2 : int(init_amount) , acn3 : int(init_amount), 
            imd_acn1 : 0 , imd_acn2 : 0,
            'debiti_'+ str(imd_acn1) + '_' + str(acn1) : 0, 'debiti_'+ str(imd_acn1) + '_' + str(acn2) : 0,
            'debiti_'+ str(imd_acn1) + '_' + str(acn3) : 0,
            'debiti_'+ str(imd_acn2) + '_' + str(acn1) : 0, 'debiti_'+ str(imd_acn2) + '_' + str(acn2) : 0,
            'debiti_'+ str(imd_acn2) + '_' + str(acn3) : 0}
    for x in range(len(transact_log)):
    #con un for mi scorro tutto transact_log
        importo = transact_log[x][1]
        # salvo in una variavile l'importo
        per = int((importo*transact_log[x][3])/100)
        #salvo in una variabile la percentuale
        # soldi_1 = reg[transact_log[x][0][0][0]]
        # soldi_2 = reg[transact_log[x][0][0][1]]
        # ag = reg[transact_log[x][0][2]]
        if importo == 0:
        #se l'importo è 0 passo
            pass
        elif importo > reg[transact_log[x][0][0]]:
        #se l'importo è maggiore dei soldi del mittente
            if (reg[transact_log[x][0][0]] - per) < 0:
            #se il mittente tolta la percentuale va in debito
               debito = reg[transact_log[x][0][0]] - per    
               #salvo il debito (calcolato sottraendo al mittente la percetuale) in una variabile
               reg[transact_log[x][2]] += reg[transact_log[x][0][0]]
               #aggiungo all'agente i soldi rimaneti nel conto del mittente
               reg['debiti_'+ str(transact_log[x][2]) + '_' + str(transact_log[x][0][0])] += debito
               #aggiungo al dizionario il debito del mittente con l'agente
               reg[transact_log[x][0][0]] = 0
               #porto a 0 il conto del mittente
            else:
            #se il mittente non va in debito
                reg[transact_log[x][2]] += per
                #do all'agente la percetuale
                reg[transact_log[x][0][0]] -= per
                #tolgo al mittente la percentuale
        elif importo <= reg[transact_log[x][0][0]]:
        #se l'importo è minore o uguale al conto del mittente
            reg[transact_log[x][0][0]] -= (importo + per)
            #tolgo al mittente l'importo + la percetuale
            if reg[transact_log[x][0][0]] < 0:
            #se il mittente tolta la percentuale va in debito
               debito = reg[transact_log[x][0][0]]
               #salvo il debito in una variabile
               reg[transact_log[x][2]] += reg[transact_log[x][0][0]] + per 
               #aggiungo all'agente i soldi rimaneti nel conto del mittente
               reg['debiti_'+ str(transact_log[x][2]) + '_' + str(transact_log[x][0][0])] += debito
               #aggiungo al dizionario il debito del mittente con l'agente
               reg[transact_log[x][0][0]] = 0
               #porto a 0 il conto del mittente
            else:
            #se il mittente non va in debito
                reg[transact_log[x][2]] += per
                #aggiungo all'agente la percetuale  
            if reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] != 0:
            # se il ricevente è indebitato con l'agente
                debito = reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] 
                debito -= importo + debito
                reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] -= debito
                reg[imd_acn1] += importo
            elif reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] != 0:
            # se il ricevente è indebitato con l'agente
                debito = reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] 
                debito -= importo + debito
                reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] -= debito
                reg[imd_acn2] += importo
            else:
            #se il ricevento non ha buffi con l'agente
                reg[transact_log[x][0][1]] += importo
                #aggiungo al ricevente i soldi dell'importo

    output =  ([reg[acn1], reg[acn2], reg[acn3]],[reg[imd_acn1], reg[imd_acn2]],[[reg['debiti_'+ str(imd_acn1) + '_' + str(acn1)],reg['debiti_'+ str(imd_acn1) + '_' + str(acn2)],reg['debiti_'+ str(imd_acn1) + '_' + str(acn3)]],[ reg['debiti_'+ str(imd_acn2) + '_' + str(acn1)], reg['debiti_'+ str(imd_acn2) + '_' + str(acn2)], reg['debiti_'+ str(imd_acn2) + '_' + str(acn3)]]])
    return output
    
    
#example1 
#ex1(0x5B23, 0xC78D, 0x44AE, 0x1612, 0x90FF, 1000,[[[17582, 23331], 800, 5650, 4], [[17582, 51085], 800, 37119, 10], [[51085, 23331], 400, 5650, 8], [[17582, 51085], 1800, 37119, 12], [[23331, 17582], 100, 5650, 2]])
#ex1(2694, 2027, 5775, 76, 242, 1000, [[[2694, 5775], 0, 242, 17], [[2027, 5775], 900, 76, 18], [[5775, 2694], 600, 76, 13], [[2027, 5775], 1100, 242, 20], [[2694, 5775], 700, 76, 4], [[2027, 5775], 1400, 76, 3], [[2694, 5775], 1000, 76, 19], [[2027, 2694], 500, 242, 17], [[5775, 2694], 1900, 76, 7], [[2027, 2694], 2800, 242, 11]])
#ex1( 3676, 645, 6042, 6, 219, 2000, [[[645, 3676], 1100, 6, 10], [[645, 3676], 1200, 219, 5], [[6042, 645], 1800, 219, 1], [[6042, 3676], 1300, 219, 0], [[645, 6042], 0, 219, 4], [[6042, 645], 0, 219, 17], [[3676, 6042], 300, 219, 11], [[645, 3676], 2000, 219, 19], [[645, 3676], 2100, 219, 12], [[6042, 3676], 2100, 219, 1], [[3676, 645], 200, 6, 19], [[6042, 3676], 900, 219, 3], [[645, 3676], 2300, 6, 14], [[6042, 3676], 500, 219, 3], [[6042, 645], 500, 6, 13], [[3676, 6042], 2300, 219, 7], [[6042, 3676], 100, 6, 0], [[6042, 3676], 2600, 6, 3], [[645, 6042], 1000, 219, 7], [[645, 6042], 1000, 6, 5], [[3676, 645], 2800, 219, 2], [[645, 3676], 2800, 219, 16], [[3676, 6042], 200, 219, 19], [[6042, 645], 2600, 219, 20], [[645, 3676], 500, 6, 9], [[3676, 645], 2200, 6, 10], [[645, 3676], 300, 6, 10], [[645, 3676], 1300, 219, 20], [[3676, 6042], 1400, 219, 7], [[6042, 645], 2500, 6, 17], [[645, 6042], 3200, 6, 9], [[6042, 3676], 1300, 6, 8], [[3676, 645], 2400, 6, 7], [[6042, 645], 100, 219, 20], [[645, 6042], 3200, 219, 14], [[645, 6042], 1700, 219, 12], [[3676, 645], 200, 6, 8], [[6042, 645], 1100, 6, 11], [[645, 6042], 700, 219, 2], [[3676, 6042], 400, 6, 14], [[645, 3676], 1900, 6, 20], [[6042, 645], 2800, 219, 9], [[645, 3676], 3200, 219, 19], [[6042, 645], 2100, 219, 11], [[3676, 645], 400, 219, 0], [[645, 3676], 3800, 6, 19], [[3676, 6042], 2700, 6, 17], [[6042, 645], 3400, 219, 2], [[6042, 3676], 1300, 219, 7], [[6042, 3676], 1600, 219, 16], [[3676, 6042], 2200, 6, 14], [[645, 3676], 1800, 219, 11], [[6042, 3676], 2700, 219, 4], [[3676, 6042], 1500, 6, 7], [[645, 6042], 1700, 6, 13], [[3676, 645], 1700, 219, 2], [[6042, 645], 900, 219, 11], [[3676, 6042], 3900, 219, 14], [[645, 6042], 400, 219, 0], [[6042, 3676], 800, 219, 7], [[645, 3676], 400, 219, 6], [[645, 3676], 1600, 219, 9], [[645, 6042], 1300, 6, 10], [[3676, 645], 3000, 219, 16], [[645, 3676], 3900, 6, 15], [[6042, 3676], 1800, 6, 12], [[645, 3676], 600, 6, 7], [[6042, 3676], 3800, 6, 4], [[645, 3676], 3200, 6, 17], [[3676, 645], 4000, 6, 10], [[6042, 645], 600, 219, 11], [[6042, 3676], 4600, 6, 6], [[645, 3676], 1000, 6, 10], [[6042, 645], 600, 6, 9], [[6042, 645], 4800, 6, 18], [[3676, 6042], 4300, 6, 19], [[645, 3676], 4900, 6, 3], [[6042, 645], 2000, 6, 10], [[645, 6042], 3500, 6, 7], [[3676, 6042], 300, 6, 19], [[645, 3676], 3900, 6, 5], [[645, 6042], 2100, 6, 8], [[6042, 3676], 700, 219, 4], [[3676, 645], 2700, 219, 19], [[645, 6042], 1800, 6, 20], [[645, 3676], 4300, 219, 17], [[3676, 645], 0, 219, 9], [[645, 3676], 5200, 219, 4], [[3676, 645], 1000, 6, 17], [[3676, 645], 700, 6, 9], [[6042, 645], 2000, 219, 7], [[6042, 3676], 400, 6, 14], [[645, 6042], 1500, 219, 0], [[6042, 645], 3700, 6, 0], [[3676, 6042], 2100, 6, 8], [[6042, 645], 4400, 219, 9], [[3676, 645], 600, 219, 16], [[6042, 3676], 3800, 219, 14], [[6042, 3676], 1900, 219, 1], [[645, 6042], 1900, 6, 2]]  )

#ex1(2694, 2027, 5775, 76, 242, 1000, [[[2694, 5775], 0, 242, 17], [[2027, 5775], 900, 76, 18], [[5775, 2694], 600, 76, 13], [[2027, 5775], 1100, 242, 20], [[2694, 5775], 700, 76, 4], [[2027, 5775], 1400, 76, 3], [[2694, 5775], 1000, 76, 19], [[2027, 2694], 500, 242, 17], [[5775, 2694], 1900, 76, 7], [[2027, 2694], 2800, 242, 11]])
#example 1
ex1(0x5B23, 0xC78D, 0x44AE, 0x1612, 0x90FF, 1000,[[[17582, 23331], 800, 5650, 4], [[17582, 51085], 800, 37119, 10], [[51085, 23331], 400, 5650, 8], [[17582, 51085], 1800, 37119, 12], [[23331, 17582], 100, 5650, 2]])

'''         
            if reg['debiti_'+ str(transact_log[x][2]) + '_' + str(transact_log[x][0][1])] != 0:
            # se il ricevento è indebitato con l'agente
                buffo = importo + reg['debiti_'+ str(transact_log[x][2]) + '_' + str(transact_log[x][0][1])]
                #calcolo il buffo sottreando all'importo il debito
                reg['debiti_'+ str(transact_log[x][2]) + '_' + str(transact_log[x][0][1])] += buffo
                #aggiungo al debito il buffo così che si elimini
                reg[transact_log[x][0][1]] += importo - buffo
                #do al mittente l'importo meno il buffo
            elif reg['debiti_'+ str(ag2) + '_' + str(transact_log[x][0][1])] != 0:
                if 1 <2:
                    reg[1] += buffo
                    reg[mitt] += importo - buffo
            elif 
            else:
            #se il ricevento non ha buffi con l'agente
                reg[transact_log[x][0][1]] += importo
                #aggiungo al ricevente i soldi dell'importo
'''
'''
            if reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] != 0 and reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] != 0:
            # se il ricevento è indebitato con l'agente
                if reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] < reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] != 0:
                    buffo = importo + reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])]
                    #calcolo il buffo sottreando all'importo il debito
                    reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] += buffo
                    #aggiungo al debito il buffo così che si elimini
                    reg[transact_log[x][0][1]] += importo - buffo
                    #do al mittente l'importo meno il buffo
                elif reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] > reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] != 0:
                    buffo = importo + reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])]
                    #calcolo il buffo sottreando all'importo il debito
                    reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] += buffo
                    #aggiungo al debito il buffo così che si elimini
                    reg[transact_log[x][0][1]] += importo - buffo
                    #do al mittente l'importo meno il buffo
                else:
                    buffo = importo + reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] + reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])]
                    #calcolo il buffo sottreando all'importo il debito
                    reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] += buffo/2
                    reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] += buffo/2
                    #aggiungo al debito il buffo così che si elimini
                    reg[transact_log[x][0][1]] += importo - buffo
                    #do al mittente l'importo meno il buffo
            elif reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] != 0:
                buffo = importo + reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])]
                #calcolo il buffo sottreando all'importo il debito
                reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] += buffo
                #aggiungo al debito il buffo così che si elimini
                reg[transact_log[x][0][1]] += importo - buffo
                #do al mittente l'importo meno il buffo
            elif reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] != 0:
                buffo = importo + reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])]
                #calcolo il buffo sottreando all'importo il debito
                reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] += buffo
                #aggiungo al debito il buffo così che si elimini
                reg[transact_log[x][0][1]] += importo - buffo
                #do al mittente l'importo meno il buffo
            else:
            #se il ricevento non ha buffi con l'agente
                reg[transact_log[x][0][1]] += importo
                #aggiungo al ricevente i soldi dell'importo
'''
'''   
# def ex1(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log):
#     output = ()
#     reg =  {acn1 : int(init_amount), acn2 : int(init_amount) , acn3 : int(init_amount), 
#             imd_acn1 : 0 , imd_acn2 : 0,
#             'debiti_'+ str(imd_acn1) + '_' + str(acn1) : 0, 'debiti_'+ str(imd_acn1) + '_' + str(acn2) : 0,
#             'debiti_'+ str(imd_acn1) + '_' + str(acn3) : 0,
#             'debiti_'+ str(imd_acn2) + '_' + str(acn1) : 0, 'debiti_'+ str(imd_acn2) + '_' + str(acn2) : 0,
#             'debiti_'+ str(imd_acn2) + '_' + str(acn3) : 0}
#     for x in range(len(transact_log)):
#     #con un for mi scorro tutto transact_log
#         importo = transact_log[x][1]
#         # salvo in una variavile l'importo
#         per = int((importo*transact_log[x][3])/100)
#         #salvo in una variabile la percentuale
#         # soldi_1 = reg[transact_log[x][0][0][0]]
#         # soldi_2 = reg[transact_log[x][0][0][1]]
#         # ag = reg[transact_log[x][0][2]]
#         if importo == 0:
#         #se l'importo è 0 passo
#             pass
#         elif importo > reg[transact_log[x][0][0]]:
#         #se l'importo è maggiore dei soldi del mittente
#             if (reg[transact_log[x][0][0]] - per) < 0:
#             #se il mittente tolta la percentuale va in debito
#                debito = reg[transact_log[x][0][0]] - per    
#                #salvo il debito (calcolato sottraendo al mittente la percetuale) in una variabile
#                reg[transact_log[x][2]] += reg[transact_log[x][0][0]]
#                #aggiungo all'agente i soldi rimaneti nel conto del mittente
#                reg['debiti_'+ str(transact_log[x][2]) + '_' + str(transact_log[x][0][0])] += debito
#                #aggiungo al dizionario il debito del mittente con l'agente
#                reg[transact_log[x][0][0]] = 0
#                #porto a 0 il conto del mittente
#             else:
#             #se il mittente non va in debito
#                 reg[transact_log[x][2]] += per
#                 #do all'agente la percetuale
#                 reg[transact_log[x][0][0]] -= per
#                 #tolgo al mittente la percentuale
#         elif importo <= reg[transact_log[x][0][0]]:
#         #se l'importo è minore o uguale al conto del mittente
#             reg[transact_log[x][0][0]] -= (importo + per)
#             #tolgo al mittente l'importo + la percetuale
#             if reg[transact_log[x][0][0]] < 0:
#             #se il mittente tolta la percentuale va in debito
#                debito = reg[transact_log[x][0][0]]
#                #salvo il debito in una variabile
#                reg[transact_log[x][2]] += reg[transact_log[x][0][0]] + per 
#                #aggiungo all'agente i soldi rimaneti nel conto del mittente
#                reg['debiti_'+ str(transact_log[x][2]) + '_' + str(transact_log[x][0][0])] += debito
#                #aggiungo al dizionario il debito del mittente con l'agente
#                reg[transact_log[x][0][0]] = 0
#                #porto a 0 il conto del mittente
#             else:
#             #se il mittente non va in debito
#                 reg[transact_log[x][2]] += per
#                 #aggiungo all'agente la percetuale  
#             if reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] != 0:
#             # se il ricevente è indebitato con l'agente
#                 debito = reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])]
#                 # salvo il debito in una variabile
#                 debito -= importo + debito
#                 # sottraggo al debito l'importo e debito stesso
#                 reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] -= debito
#                 reg[imd_acn1] += importo
#             elif reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] != 0:
#             # se il ricevente è indebitato con l'agente
#                 debito = reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] 
#                 debito -= importo + debito
#                 reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] -= debito
#                 reg[imd_acn2] += importo
#             elif reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] and reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] != 0:
#                 if reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] < reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])]:
#                     #do i soldi al primo e se avanzano al secondo
#                     debito = reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] 
                    
#                     debito -= importo + debito
#                     reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] -= debito
#                     reg[imd_acn1] += importo 
#                 elif reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] > reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])]:
#                     debito = reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] 
#                     debito -= importo + debito
#                     reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] -= debito
#                     reg[imd_acn2] += importo
#                 elif reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] == reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])]:
#                     reg['debiti_'+ str(imd_acn1) + '_' + str(transact_log[x][0][1])] += importo/2
#                     reg['debiti_'+ str(imd_acn2) + '_' + str(transact_log[x][0][1])] += importo/2
#             else:
#             #se il ricevento non ha buffi con l'agente
#                 reg[transact_log[x][0][1]] += importo
#                 #aggiungo al ricevente i soldi dell'importo

#     output =  ([reg[acn1], reg[acn2], reg[acn3]],[reg[imd_acn1], reg[imd_acn2]],[[reg['debiti_'+ str(imd_acn1) + '_' + str(acn1)],reg['debiti_'+ str(imd_acn1) + '_' + str(acn2)],reg['debiti_'+ str(imd_acn1) + '_' + str(acn3)]],[ reg['debiti_'+ str(imd_acn2) + '_' + str(acn1)], reg['debiti_'+ str(imd_acn2) + '_' + str(acn2)], reg['debiti_'+ str(imd_acn2) + '_' + str(acn3)]]])
#     return output
    














'''
def es1(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log):
    output = ()
    reg =  {acn1 : int(init_amount), acn2 : int(init_amount) , acn3 : int(init_amount), 
            imd_acn1 : 0 , imd_acn2 : 0,
            'debiti_'+ str(imd_acn1) + '_' + str(acn1) : 0, 'debiti_'+ str(imd_acn1) + '_' + str(acn2) : 0,
            'debiti_'+ str(imd_acn1) + '_' + str(acn3) : 0,
            'debiti_'+ str(imd_acn2) + '_' + str(acn1) : 0, 'debiti_'+ str(imd_acn2) + '_' + str(acn2) : 0,
            'debiti_'+ str(imd_acn2) + '_' + str(acn3) : 0}
    #creo un dizionario in cui assegno ad ogni variabile il suo valore
    for x in range(len(transact_log)):
    #utilizzo un for per scorrere tutte le transazioni all'interno di transact_log
        costo = transact_log[x][1]       
        soldi_1 = reg[transact_log[x][0][0]]
        soldi_2 = reg[transact_log[x][0][1]]
        soldi_agente = reg[transact_log[x][2]]
        agente = transact_log[x][2]
        per = int(round((costo*transact_log[x][3])/100))
        #salvo l'importo, i conti degli intermediari, il conto dell'agente e l'identità dell'agente all'interno
        #in variabili fisse così da non doverle ricercare ogni volta
        if costo == 0:
        #se il costo della transazione è 0 passo direttamente alla prossima transazione
            pass
        elif costo <= (soldi_1):                        
        #se l'importo è minore o uguale del conto del mittente
            soldi_1 -= (costo + per)
            #tolgo al mittente il costo della totale della transazione
            if soldi_1 < 0:
            #se il mittente cade in debito a causa della %
               soldi_agente += (per+soldi_1)
               #do all'agente i soldi rimantenti nel conto del mittente               
               if transact_log[x][0][0] == acn1:
               #aggiungo il debito nel dizionario
                  reg['debiti_'+ str(agente) + '_' + str(transact_log[x][0][0])] += int(soldi_1)
               elif transact_log[x][0][0] == acn2:
                  reg['debiti_'+ str(agente) + '_' + str(transact_log[x][0][0])] += int(soldi_1)
               else:
                  reg['debiti_'+ str(agente) + '_' + str(transact_log[x][0][0])] += int(soldi_1)
               soldi_1 = 0 
               #porto a 0 il conto del mittente
               if reg['debiti_'+ str(agente) + '_' + str(transact_log[x][0][1])] > 0 :
               #se il ricevente non è indebitato con l'agente
                   soldi_2 += costo
                   #aggiungo al ricevente il costo
               else:
               #se il ricevente è indebitato con l'agente
                   
                   resto = costo+reg['debiti_'+ str(agente) + '_' + str(transact_log[x][0][1])]
                   #mi calcolo il resto (costo-debito)
                   soldi_2 += resto
                   #aggiungo il resto al ricevente
                   debito = (costo - resto)
                   #mi calcolo il debito (costo-resto)                   
                   soldi_agente +=  debito
                   #lo aggiungo all'agente
               #aggiungo al conto del ricevente i soldi della transazione
               reg[transact_log[x][0][0]] = soldi_1
               reg[transact_log[x][0][1]] = soldi_2
               reg[transact_log[x][2]] = soldi_agente   
               #aggiorno i valori nel dizionario
            else:
            #se il mittente non va in debito
                if reg['debiti_'+ str(agente) + '_' + str(transact_log[x][0][1])] > 0:
                   soldi_2 += costo
                else:
                   resto = costo+reg['debiti_'+ str(agente) + '_' + str(transact_log[x][0][1])]
                   debito = (costo - resto)
                   soldi_agente +=  debito
                   soldi_2 += resto
                #aggiungo al conto del ricevente i soldi della transazione
                soldi_agente += per
                #aggiungo al conto dell'agente i soldi della %
                reg[transact_log[x][0][0]] = soldi_1
                reg[transact_log[x][0][1]] = soldi_2
                reg[transact_log[x][2]] = soldi_agente    
                #aggiorno i valori nel dizionario
        else:
            soldi_1 -= per
            if soldi_1 < 0:
                soldi_agente += (per+soldi_1)
                if transact_log[x][0][0] == acn1:
                #aggiungo il debito nel dizionario
                  reg['debiti_'+ str(agente) + '_' + str(transact_log[x][0][0])] += int(soldi_1)
                elif transact_log[x][0][0] == acn2:
                  reg['debiti_'+ str(agente) + '_' + str(transact_log[x][0][0])] += int(soldi_1)
                else:
                  reg['debiti_'+ str(agente) + '_' + str(transact_log[x][0][0])] += int(soldi_1)
                soldi_1 = 0
                reg[transact_log[x][0][0]] = soldi_1
                reg[transact_log[x][0][1]] = soldi_2
                reg[transact_log[x][2]] = soldi_agente
            else:
                soldi_agente += per
                reg[transact_log[x][0][0]] = soldi_1
                reg[transact_log[x][0][1]] = soldi_2
                reg[transact_log[x][2]] = soldi_agente
    output =  ([reg[acn1], reg[acn2], reg[acn3]],[reg[imd_acn1], reg[imd_acn2]],[[reg['debiti_'+ str(imd_acn1) + '_' + str(acn1)],reg['debiti_'+ str(imd_acn1) + '_' + str(acn2)],reg['debiti_'+ str(imd_acn1) + '_' + str(acn3)]],[ reg['debiti_'+ str(imd_acn2) + '_' + str(acn1)], reg['debiti_'+ str(imd_acn2) + '_' + str(acn2)], reg['debiti_'+ str(imd_acn2) + '_' + str(acn3)]]])
    return output
'''
if __name__ == '__main__':
    # Insert your own tests here
    pass
