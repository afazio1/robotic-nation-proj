import sqlite3

#DB연결
conn = sqlite3.connect("./artistDB.db")
c = conn.cursor()

#CREATE
def CREATE() :
    #테이블 생성
    c.execute("CREATE TABLE IF NOT EXISTS ARTIST(NAME TEXT, URI TEXT PRIMARY KEY)")

    #샘플 데이터 삽입
    c.execute("INSERT INTO ARTIST VALUES('IZ*ONE', 'spotify:artist:5r1tUTxVSgvBHnoDuDODPH')")    #IZ*ONE
    c.execute("INSERT INTO ARTIST VALUES('AKMU', 'spotify:artist:6OwKE9Ez6ALxpTaKcT5ayv')")      #AKMU
    c.execute("INSERT INTO ARTIST VALUES('GFRIEND', 'spotify:artist:0qlWcS66ohOIi0M8JZwPft')")   #GFRIEND
    c.execute("INSERT INTO ARTIST VALUES('Lovelyz', 'spotify:artist:3g34PW5oNmDBxMVUTzx2XK')")   #Lovelyz
    c.execute("INSERT INTO ARTIST VALUES('TAEYEON', 'spotify:artist:3qNVuliS40BLgXGxhdBdqu')")   #TAEYEON
    c.execute("INSERT INTO ARTIST VALUES('(G)I-DLE', 'spotify:artist:2AfmfGFbe0A0WsTYm0SDTx')")  #(G)I-DLE
    c.execute("INSERT INTO ARTIST VALUES('IU', 'spotify:artist:3HqSLMAZ3g3d5poNaI7GOU')")        #IU
    c.execute("INSERT INTO ARTIST VALUES('BTS', 'spotify:artist:3Nrfpe0tUJi4K4DXYWgMUX')")       #BTS
    c.execute("INSERT INTO ARTIST VALUES('OhMyGirl', 'spotify:playlist:3vY95dpjxt4Tzgg8AIf707')")#OhMyGirl
    c.execute("INSERT INTO ARTIST VALUES('Davichi', 'spotify:artist:4z6yrDz5GfKXkeQZjOaZdq')")   #Davichi
    c.execute("INSERT INTO ARTIST VALUES('BOL4', 'spotify:artist:4k5fFEYgkWYrYvtOK3zVBl')")      #BOL4
    c.execute("INSERT INTO ARTIST VALUES('Noel', 'spotify:artist:2G5VFTwwlZUulCbtPbc1nx')")      #Noel
    c.execute("INSERT INTO ARTIST VALUES('CHUNG HA', 'spotify:artist:2PSJ6YriU7JsFucxACpU7Y')")  #CHUNG HA
    c.execute("INSERT INTO ARTIST VALUES('APRIL', 'spotify:artist:4cJ99wTjC60pXcfyISL9fa')")     #APRIL
    c.execute("INSERT INTO ARTIST VALUES('AILEE', 'spotify:artist:3uGFTJ7JMllvhgGpumieHF')")     #AILEE
    c.execute("INSERT INTO ARTIST VALUES('Epik High', 'spotify:artist:5snNHNlYT2UrtZo5HCJkiw')") #Epik High
    c.execute("INSERT INTO ARTIST VALUES('Lee Soo', 'spotify:artist:0wJ9JgzAlq9nif4ye4WrAR')")   #Lee Soo
    c.execute("INSERT INTO ARTIST VALUES('BLACKPINK', 'spotify:artist:41MozSoPIsD1dJM0CLPjZF')") #BLACKPINK
    c.execute("INSERT INTO ARTIST VALUES('ITZY', 'spotify:artist:2KC9Qb60EaY0kW4eH68vr3')")      #ITZY
    c.execute("INSERT INTO ARTIST VALUES('iKON', 'spotify:artist:5qRSs6mvI17zrkJpOHkCoM')")      #iKON
    c.execute("INSERT INTO ARTIST VALUES('Red Velvet', 'spotify:artist:1z4g3DjTBBZKhvAroFlhOM')")#Red Velvet
    c.execute("INSERT INTO ARTIST VALUES('BTOB', 'spotify:artist:2hcsKca6hCfFMwwdbFvenJ')")      #BTOB
    c.execute("INSERT INTO ARTIST VALUES('SEVENTEEN', 'spotify:artist:7nqOGRxlXj7N2JYbgNEjYH')") #SEVENTEEN
    c.execute("INSERT INTO ARTIST VALUES('GOT7', 'spotify:artist:6nfDaffa50mKtEOwR8g4df')")      #GOT7
    c.execute("INSERT INTO ARTIST VALUES('Monsta X', 'spotify:artist:4TnGh5PKbSjpYqpIdlW5nz')")  #Monsta X
    c.execute("INSERT INTO ARTIST VALUES('TWICE', 'spotify:artist:7n2Ycct7Beij7Dj7meI4X0')")     #TWICE
    c.execute("INSERT INTO ARTIST VALUES('N.Flying', 'spotify:artist:2ZmXexIJAD7PgABrj0qQRb')")  #N.Flying
    c.execute("INSERT INTO ARTIST VALUES('SUNMI', 'spotify:artist:6MoXcK2GyGg7FIyxPU5yW6')")     #SUNMI
    c.execute("INSERT INTO ARTIST VALUES('Yang Da Il', 'spotify:artist:5DnjOSzLCfn4hDbLECq8pt')")#Yang Da Il
    c.execute("INSERT INTO ARTIST VALUES('BEN', 'spotify:artist:0bDdOBGVCFVt0f8N9ldW1k')")       #BEN
    c.execute("INSERT INTO ARTIST VALUES('Paul Kim', 'spotify:artist:4qRXrzUmdy3p33lgvJEzdv')")  #Paul Kim
    conn.commit()

    print("Insertion Completed")

#READ
def READ() :
    i = 1
    buf = str()
    for row in c.execute("SELECT NAME FROM ARTIST") :
        buf = buf + '[' + str(i) + ']' + ' ' + ''.join(row) + '\n'
        i += 1
    print(buf)
    return buf

#UPDATE
def UPDATE() :
    NAME = input("Enter Target Artist Name : ")
    URI = input("Enter Target Artist URI : ")
    c.execute("UPDATE ARTIST SET NAME = ? WHERE URI = ?", (NAME, URI))
    

#DELETE
def DELETE() :
    INPUT_NAME = input("Enter Target Artist Name : ")
    # c.execute("DELETE URI FROM ARTIST WHERE NAME = :NAME", {"NAME" : INPUT_NAME})
    deleted_rows = conn.execute("DELETE URI FROM ARTIST WHERE NAME = :NAME", {"NAME" : INPUT_NAME}).rowcount
    if deleted_rows > 0 :
        print("Deletion Completed. {} rows" .format(deleted_rows))
    else :
        print("Deletion Failed. No rows to delete")

#RETRIEVE
def RETRIEVE() :
    INPUT_NAME = input("Enter Target Artist Name : ")
    c.execute("SELECT URI FROM ARTIST WHERE NAME = :NAME", {"NAME" : INPUT_NAME})
    RSLT = c.fetchone()
    if RSLT :
        print(RSLT[0])
        return RSLT[0]
    else :
        print("No results found")
        return 'N/A'

def print_menu() :
    print()
    print("1. CREATE")
    print("2. READ")
    print("3. UPDATE")
    print("4. DELETE")
    print("5. RETRIEVE")
    print("6. Exit")
    print()

def main() :
    while True :
        print_menu()
        menu = int(input("Select Menu Number : "))
        if menu == 1 :
            CREATE()
        elif menu == 2 :
            READ()
        elif menu == 3 :
            UPDATE()
        elif menu == 4 :
            DELETE()
        elif menu == 5 :
            RETRIEVE()
        else :
            print("EXIT..")
            break

if __name__ == "__main__" :
    main()