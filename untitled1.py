# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 22:37:35 2021

@author: zgale
"""

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
    
    for transaction in transact_log:
        #con un for mi scorro tutto transact_log
        importo = transaction[1]
        # salvo in una variavile l'importo
        per = int((importo*transaction[3])/100)
        #salvo in una variabile la percentuale
        if importo == 0:
        #se l'importo è 0 passo
            continue
        mittente = transaction[0][0]
        intermediario = transaction[2]
        ricevente = transaction[0][1]
        
        #se il mittente meno l'importo + percentuale è > 0 (ha abbastanza soldi) levo i soldi al mittente
        if importo + per <= saldo_giocatore[mittente]:
            saldo_giocatore[mittente] -= importo + per
            guadagno_intermediario[intermediario] += per
            
            #se il ricevente non è in debito con nessuno aggiungo al ricevente l'importo intero
            if debiti[(ricevente, imd_acn1)] == 0 and debiti[(ricevente, imd_acn2)] == 0:
                saldo_giocatore[ricevente] += importo
             
            #se il ricevente è in debito con l'intermediario1 ma non con il secondo 
            #calcolo il debito del ricevente con l'intermediario1
            #calcolo i soldi che devono rientrare al ricevente
            elif debiti[(ricevente, imd_acn1)] != 0 and debiti[(ricevente, imd_acn2)] == 0: 
                  guadagno_ricevente = importo + debiti[(ricevente, imd_acn1)]
                 
                 
                  #se il guadagno del ricevente è positivo ho pagato tutto il debito e 
                  #i soldi che avanzano li do al ricevente
                  #calcolo il guadagno dell'agente sommandogli i debiti  e sommo la stessa cifra all'intermediario
                  if  guadagno_ricevente >= 0:
                      guadagno_agente = -debiti[(ricevente, imd_acn1)] 
                      saldo_giocatore[ricevente] += guadagno_ricevente
                      guadagno_intermediario[imd_acn1] += guadagno_agente 
                      debiti[(ricevente, imd_acn1)] = 0
                    
                  #sennò li do solo all'intermediario
                  else: 
                      guadagno_intermediario[imd_acn1] += importo
                      debiti[(ricevente, imd_acn1)] += importo
                     
            #se il ricevente è in debito con l'intermediario2 ma non con il primo 
            elif debiti[(ricevente, imd_acn1)] == 0 and debiti[(ricevente, imd_acn2)] != 0:
                  guadagno_ricevente = importo + debiti[(ricevente, imd_acn2)]
                 
                 
                  #se il guadagno del ricevente è positivo ho pagato tutto il debito e 
                  #i soldi che avanzano li do al ricevente
                  if  guadagno_ricevente >= 0:
                      guadagno_agente = -debiti[(ricevente, imd_acn2)] 
                      saldo_giocatore[ricevente] += guadagno_ricevente
                      guadagno_intermediario[imd_acn2] += guadagno_agente
                      debiti[(ricevente, imd_acn2)] = 0
                     
                  #sennò li do solo all'intermediario
                  else: 
                      guadagno_intermediario[imd_acn2] += importo
                      debiti[(ricevente, imd_acn2)] += importo
                     
            #se il ricevente ha debiti con entrambi
            else:         
                # se il debito dell'intermediario uno è maggiore del secondo
                #calcolo il guadagno dell'intermediario 2
                if debiti[(ricevente, imd_acn1)] < debiti[(ricevente, imd_acn2)]:
                    guadagno_imd_acn2 = importo + debiti[(ricevente, imd_acn1)]
                    
                    # se il guadagno del agente 2 è positivo ho pagato tutto il debito con l'agente1
                    # i soldi che avanzano li da all'agente2
                    if guadagno_imd_acn2 >= 0:
                        guadagno_imd_acn1 = -debiti[(ricevente, imd_acn1)]
                        guadagno_intermediario[imd_acn2] += guadagno_imd_acn2
                        guadagno_intermediario[imd_acn1] += guadagno_imd_acn1
                        debiti[(ricevente, imd_acn1)] = 0
                        guadagno_ricevente = importo + debiti[(ricevente, imd_acn2)]
                        
                        if guadagno_ricevente >= 0:
                            guadagno_imd_acn2 = -debiti[(ricevente, imd_acn2)]
                            saldo_giocatore[ricevente] += guadagno_ricevente
                            guadagno_intermediario[imd_acn2] += guadagno_imd_acn2()
                            debiti[(ricevente, imd_acn2)] = 0
                        else:
                            guadagno_intermediario[imd_acn2] += importo
                            debiti[(ricevente, imd_acn1)] += importo
                            
                    else:
                        guadagno_intermediario[imd_acn1] += -debiti[(ricevente, imd_acn1)] + debiti[(ricevente, imd_acn2)]
                        debiti[(ricevente, imd_acn1)] += -debiti[(ricevente, imd_acn1)] + debiti[(ricevente, imd_acn2)]
                
                #se il debito di imd_acn2 è maggiore del debito di imd_acn1
                elif debiti[(ricevente, imd_acn1)] > debiti[(ricevente, imd_acn2)]:  
                    guadagno_imd_acn1 = importo + debiti[(ricevente, imd_acn2)]
                    
                    # se il guadagno del agente 2 è positivo ho pagato tutto il debito con l'agente1
                    # i soldi che avanzano li da all'agente2
                    if guadagno_imd_acn1 >= 0:
                        guadagno_imd_acn2 = -debiti[(ricevente, imd_acn2)]
                        guadagno_intermediario[imd_acn1] += guadagno_imd_acn1
                        guadagno_intermediario[imd_acn2] += guadagno_imd_acn2
                        debiti[(ricevente, imd_acn2)] = 0
                        guadagno_ricevente = importo + debiti[(ricevente, imd_acn1)]
                        
                        if guadagno_ricevente >= 0:
                            guadagno_imd_acn1 = -debiti[(ricevente, imd_acn1)]
                            saldo_giocatore[ricevente] += guadagno_ricevente
                            guadagno_intermediario[imd_acn1] += guadagno_imd_acn1
                            debiti[(ricevente, imd_acn1)] = 0
                        else:
                            guadagno_intermediario[imd_acn1] += importo
                            debiti[(ricevente, imd_acn2)] += importo
                            
                    else:
                        guadagno_intermediario[imd_acn2] += -debiti[(ricevente, imd_acn2)] + debiti[(ricevente, imd_acn1)]
                        debiti[(ricevente, imd_acn2)] += -debiti[(ricevente, imd_acn2)] + debiti[(ricevente, imd_acn1)]
                
                # se il debito di imd_acn1 e imd_acn2 sono uguali
                else:
                    debiti[(ricevente, imd_acn1)] += importo/2
                    debiti[(ricevente, imd_acn2)] += importo/2
                    #entrambi pagati troppo
                    if debiti[(ricevente, imd_acn1)] and debiti[(ricevente, imd_acn2)] > 0:
                        saldo_giocatore[ricevente] += debiti[(ricevente, imd_acn1)] + debiti[(ricevente, imd_acn2)]
                        debiti[(ricevente, imd_acn1)] = 0
                        debiti[(ricevente, imd_acn2)] = 0
                    #intermediario1 pagato troppo
                    elif debiti[(ricevente, imd_acn1)] > 0 and debiti[(ricevente, imd_acn2)] <= 0:
                          saldo_giocatore[ricevente] += debiti[(ricevente, imd_acn1)]
                          debiti[(ricevente, imd_acn1)] = 0
                    #intermediario2 pagato troppo
                    elif debiti[(ricevente, imd_acn1)] <= 0 and debiti[(ricevente, imd_acn2)] > 0:
                          saldo_giocatore[ricevente] += debiti[(ricevente, imd_acn2)]
                          debiti[(ricevente, imd_acn2)] = 0
                    else:
                        continue
        #se il mittente non ha abbastanza soldi per la transazione (il ricevente non vedde uno spiccio)
        #ma l'intermediario se pia comunque li sordi               
        else: 
            #tolgo i soldi della per al mittente
            saldo_giocatore[mittente] -= per
            
            #se il mittente non va in debito aggiungo i soldi all'intermediario
            if saldo_giocatore[mittente] >= 0:
                guadagno_intermediario[intermediario] += per
                
            #se il mittente va in debito aggiungo all'intermediario la per meno i soldi mancanti al mittente
            #aggiungo ai debiti i soldi mancanti dalla per
            #porto a 0 i soldi del mittenten
            else:
                guadagno_intermediario[intermediario] += per + saldo_giocatore[mittente]
                debiti[(ricevente, intermediario)] += saldo_giocatore[mittente]
                saldo_giocatore[mittente] = 0         
    output =  ([saldo_giocatore[acn1], saldo_giocatore[acn2], saldo_giocatore[acn3]],
                [guadagno_intermediario[imd_acn1], guadagno_intermediario[imd_acn2]],
                [[debiti[(acn1, imd_acn1)], debiti[(acn2, imd_acn1)], debiti[(acn3, imd_acn1)]]],
                [[debiti[(acn1, imd_acn2)], debiti[(acn2, imd_acn2)], debiti[(acn3, imd_acn2)]]])  
    return output          