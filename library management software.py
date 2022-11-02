
try:
    con,cur=None,None
    def sql_connection():
          global con,cur
          import mysql.connector as sqlcon
          con=sqlcon.connect(host='localhost',user='root',passwd='fg3*d12',database='library')
          if con.is_connected():
                print('connected to mysql')
          else:
                print('connection to mysql interrupted')
                return

          cur=con.cursor()
                              
    def booksearch():
        search='''
                                        --------------------------------------------------
                                                        Book search
                                        --------------------------------------------------
                                                       '''
        print(search)
        print('enter details of book to search')
        bookname=input('Book name: ')
        genre=input('Genre: ')
        author=input('Author: ')
        version=input('Version: ')
        publication=input('Publication: ')
        books='''select bookno,bookname,author,genre,version,publication,location from books
                 where bookname='{}' or genre='{}' or author='{}' or version='{}' or
                 publication='{}';'''.format(bookname,genre,author,version,publication)
        cur.execute(books)
        data=cur.fetchall()
        if data==[]:
             print('Book is not available')
        else:        
             table='''
+-----------------+-------------------------+-----------------+-----------------+----------+---------------+---------+
|Bookno    |Book name                |Author           |genre            |version   |publication    |location |
+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+'''
             d='''|%1s|%25s|%17s|%17s|%10s|%15s|%9s|'''
             print(table)                                  
             for row in data:
                   print(d%(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
             else:
                 print('''+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+''')
                 
    def books_in_use(): 
        st='''select bookno,bookname,author,genre,version,publication,location,borrowedby,dateborrowed from books where availability='no';'''
        cur.execute(st)
        data3=cur.fetchall()
        table='''
+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+-----------+-------------+
|Bookno    |Book name                |Author           |genre            |version   |publication    |location |borrowedby |dateborrowed |
+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+-----------+-------------+'''
        d='''|%10s|%25s|%17s|%17s|%10s|%15s|%9s|%11s|%13s|'''
        print(table)
        for row in data3:
             print(d%(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
        else:
             print('''+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+-----------+-------------+''')

    def add_new_books():
        bookno=int(input('Bookno: '))
        bookname=input('Bookname: ')
        author=input('Author: ')
        genre=input('Genre: ')
        version=input('Version: ')
        publication=input('Publication: ')
        location=input('Location: ')
        st1='''select * from books where bookno='{}';'''.format(bookno)
        cur.execute(st1)
        data4=cur.fetchall()
        n=cur.rowcount
        if n!=0:
            print('The book already exists')
        else:
            st2='''insert into books(bookno,bookname,author,genre,version,publication,location,availability)
                   values('{}','{}','{}','{}','{}','{}','{}','{}');'''.format(bookno,bookname,author,genre,version,publication,location,'yes')
            cur.execute(st2)
            con.commit()
    def delete_books():
        bookno=int(input('Enter bookno of the book to be deleted: '))
        st1='''select * from books where bookno='{}';'''.format(bookno)
        cur.execute(st1)
        cur.fetchall()
        n=cur.rowcount
        if n==0:
            print('The book does not exist')
        else:
            st2='''delete from books where bookno='{}';'''.format(bookno)
            cur.execute(st2)
            con.commit()
            print('Book is removed from library') 
    def members():
      qs='''select id,name,streamdepartment from members order by id asc;'''
      cur.execute(qs)
      data=cur.fetchall()
      table='''
+----------+------------------------------+--------------------+
|ID        |Name                          |stream/department   |
+----------+------------------------------+--------------------+'''
      print(table)
      d='''|%10s|%30s|%20s|'''
      for row in data:
            print(d%(row[0],row[1].capitalize(),row[2].capitalize()))
      else:
          print('+----------+------------------------------+--------------------+')
          
    def del_members():
          ID=input("Enter an ID starting with 'ST/','TE/' or 'AD/': ").upper()
          qs='''select * from members where ID='{}';'''.format(ID)
          cur.execute(qs)
          data=cur.fetchall()
          n=cur.rowcount
          if n==0:
                print('The given ID does not exist')
          else:
                sq='''delete from members where id='{}';'''.format(ID)
                cur.execute(sq)
                con.commit()
                print()
                print('Account',ID,'is deleted')
                
    def complaint():
          qs='''select * from complaints order by sno asc;'''
          cur.execute(qs)
          data=cur.fetchall()
          table='''
+----+------------+-----------------------------------------------------------------------------------------------------------------+
|S.no|Date        |Complaint                                                                                                        |
+----+------------+-----------------------------------------------------------------------------------------------------------------+'''
          print(table)
          d='''|%4s|%12s|%113s|'''   
          for row in data:
                print(d%(row[0],row[1],row[2]))
          else:
              print('+----+------------+-----------------------------------------------------------------------------------------------------------------+')
              
    def user_activity():
          qs='''select id,name,bookname,dateborrowed from members M,books B where M.id=B.borrowedby order by B.dateborrowed asc;'''
          cur.execute(qs)
          data=cur.fetchall()
          table='''
+----------+----------------------------+---------------------------+------------+
|ID        |Name                        |Bookname                   |dateborrowed|
+----------+----------------------------+---------------------------+------------+'''
          print(table)
          d='''|%10s|%28s|%27s|%12s|'''
          for row in data:
                print(d%(row[0],row[1].capitalize(),row[2].capitalize(),row[3]))
          else:
              print('+----------+----------------------------+---------------------------+------------+')
    def fine_read():
        st='''select bookno,borrowedby,dateborrowed from books where availability='no';'''
        cur.execute(st)
        data=cur.fetchall()
        for row in data:
              if 'ST/' in row[1]:
                    fine=0
                    sq='''select round(datediff(curdate(),dateborrowed)) as time_taken from books where bookno='{}';'''.format(row[0])
                    cur.execute(sq)
                    i=cur.fetchall()
                    n=i[0][0]
                    m=n-5
                    if m<=0:
                       fine=fine+5
                    else:
                       fine=fine+5+(12.5/10)**m
                    m='''update books set fine={} where bookno='{}';'''.format(fine,row[0])
                    cur.execute(m)
                    con.commit()
              elif 'TE/' in row[1]:
                    fine=0
                    sq='''select round(datediff(curdate(),dateborrowed)) as time_taken from books where bookno='{}';'''.format(row[0])
                    cur.execute(sq)
                    i=cur.fetchall()
                    n=i[0][0]
                    m=n-5
                    if m<=0:
                       fine=0
                    else:
                       fine=fine+(12.5/10)**m
                    m='''update books set fine={} where bookno='{}';'''.format(fine,row[0])
                    cur.execute(m)
                    con.commit()
              elif 'AD/' in row[1]:
                    fine=0
                    sq='''select round(datediff(curdate(),dateborrowed)) as time_taken from books where bookno='{}';'''.format(row[0])
                    cur.execute(sq)
                    i=cur.fetchall()
                    n=i[0][0]
                    m=n-5
                    if m<=0:
                       fine=0
                    else:
                       fine=fine+(12.5/10)**m
                    m='''update books set fine={} where bookno='{}';'''.format(fine,row[0])
                    cur.execute(m)
                    con.commit()
              else:
                  continue
    def transactions():
              ID=input('''Enter the ID followed by 'ST/' or 'TE/' or 'AD/': ''').upper()
              account='''select id from members where id='{}'; '''.format(ID)
              cur.execute(account)
              d=cur.fetchall()
              if d==[]:
                    print('ID does not exist')
              elif ID==d[0][0]:
                    qs='''select bookno,bookname,dateborrowed,fine from books where borrowedby='{}'; '''.format(ID)
                    cur.execute(qs)
                    data=cur.fetchall()
                    table='''
+--------+----------------------------+-------------+-------+
|Bookno  |Book name                   |Date borrowed| Fines |
+--------+----------------------------+-------------+-------+'''
                    print(table)
                    d='''|%8s|%28s|%13s|%7s|'''
                    amount=0    
                    for row in data:
                          print(d%(row[0],row[1],row[2],row[3]))
                          amount+=row[3]
                    else:
                          print('+--------+----------------------------+-------------+-------+')
                          print()
                          if amount>0:
                                print('Total amount payable by',ID,': ',amount)
                                pay=input('Is the payment given? y/n: ')
                                if pay=='y':
                                      a='''update books set availability='yes' where borrowedby='{}';'''.format(ID)
                                      b='''update books set fine=0.00 where borrowedby='{}';'''.format(ID)
                                      c='''update books set dateborrowed='0000/00/00' where borrowedby='{}';'''.format(ID)
                                      d='''update books set borrowedby='' where borrowedby='{}';'''.format(ID)
                                      cur.execute(a)
                                      cur.execute(b)
                                      cur.execute(c)
                                      cur.execute(d)
                                      con.commit()
                                      from datetime import date                              
                                      date=date.today()
                                      n='''select * from payments; '''
                                      cur.execute(n)
                                      data=cur.fetchall()
                                      sno_count=cur.rowcount
                                      sno=sno_count+1
                                      p='''insert into payments(sno,date,id,amount)
                                           values({},'{}','{}',{});'''.format(sno,date,ID,amount)
                                      cur.execute(p)
                                      con.commit()
                                      print('Fines of',ID,'was successfully paid')
                                      
                          else:
                              print('There is no fine')
              else:
                    print('ID does not exist')
     
    while True:
          print()
          first='''                                     LIBRARY MANAGEMENT SOFTWARE

 '''
          print(first)
          user=input("Press enter to continue or type 'exit' to exit ")
          if user.lower()=='exit':
              break
          else:
              login='''
                             SIGNIN AS
                        ---------------------
                        1.Student
                        2.Teacher
                        3.Admin
                        4.create new account'''


              print(login)
              login_as=int(input('signin as: '))

              if login_as==1:
                    sql_connection()
                    username=input('Username: ')
                    user_search='''select * from members
                                   where username='{}' and id like 'ST%';'''.format(username)

                    cur.execute(user_search)
                    data=cur.fetchall()
                    n=cur.rowcount
                    if n==0:
                        print('username does not exist')
                        continue
                    else:
                         password=input('Password: ')
                         passwd_search='''select password from members
                                          where username='{}';'''.format(username)
                         cur.execute(passwd_search)
                         data=cur.fetchall()
                         if password==data[0][0]:
                             while True:
                                   menu='''
                                        
                                                             MENU
                                        --------------------------------------------------
                                             1.Books
                                             2.My books
                                             3.My account
                                             4.Fines 
                                             5.Rules and regulations
                                             6.Suggestions and complaints
                                             7.sign out
                                             '''
                                   print(menu)
                                   choice=int(input('select your choice: '))
                                   if choice==1:
                                         menu='''
                                        --------------------------------------------------
                                                            Books
                                        --------------------------------------------------
                                                  1.Display all books
                                                  2.Search
                                                   '''
                                         print(menu)
                                         choice=int(input('select your choice: '))
                                         if choice==1:
                                               sql_connection()
                                               books='''select bookno,bookname,author,genre,version,publication,location from books;'''
                                               cur.execute(books)
                                               data=cur.fetchall()
                                               table='''
+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+
|Bookno    |Book name                |Author           |genre            |version   |publication    |location |
+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+'''
                                               d='''|%10s|%25s|%17s|%17s|%10s|%15s|%9s|'''

                                               print(table)
                                               for row in data:
                                                     print(d%(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
                                               else:
                                                       print('''+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+''')
                                                       print()
                                                       print()
                                                       input('press enter to go to main menu')
                                         elif choice==2:
                                               booksearch()
                                               print()
                                               print()
                                               input('press enter to go to main menu')
                                         else:
                                               print('Invalid choice. Try again')
                                   elif choice==2:
                                       print('''
                                        --------------------------------------------------
                                                            MY BOOKS
                                        --------------------------------------------------''')
                                       print()
                                       account='''select id from members
                                                  where username='{}'and password='{}';'''.format(username,password)

                                       cur.execute(account)
                                       data=cur.fetchall()
                                       ID=data[0][0]
                                       books='''select bookno,bookname,author,genre,version,publication,location,dateborrowed from books where borrowedby='{}';'''.format(ID)
                                       cur.execute(books)
                                       data=cur.fetchall()
                                       table='''
+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+-------------+
|Bookno    |Book name                |Author           |genre            |version   |publication    |location |dateborrowed |
+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+-------------+'''
                                       d='''|%10s|%25s|%17s|%17s|%10s|%15s|%9s|%13s|'''
                                       print(table)
                                       for row in data:
                                             print(d%(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
                                       else:
                                            print('''+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+-------------+''')
                                            print()
                                            print()
                                            input('press enter to go to main menu')
                                            
                                   elif choice==4:
                                       fine_read()
                                       print(''' 
                                        --------------------------------------------------
                                                            FINES
                                        --------------------------------------------------''')
                                       print()
                                       account='''select id from members
                                                  where username='{}'and password='{}';'''.format(username,password)
                                       cur.execute(account)
                                       d=cur.fetchall()
                                       ID=d[0][0]
                                       qs='''select bookno,bookname,dateborrowed,fine from books
                                             where borrowedby='{}';'''.format(ID)
                                       cur.execute(qs)
                                       data=cur.fetchall()
                                       table='''
+--------+----------------------------+-------------+-------+
|Bookno  |Book name                   |Date borrowed| Fines |
+--------+----------------------------+-------------+-------+'''
                                       print(table)
                                       d='''|%8s|%28s|%13s|%7s|'''
                                       amount=0    
                                       for row in data:
                                           print(d%(row[0],row[1],row[2],row[3]))
                                           amount+=row[3]
                                       else:
                                           print('+--------+----------------------------+-------------+-------+')
                                           print()
                                           print('Total fine payable: ',amount)
                                           print()
                                           input('Press enter to continue') 
                                           
                                   elif choice==3:
                                       account='''select id,name,streamdepartment from members
                                                  where username='{}'and password='{}';'''.format(username,password)

                                       cur.execute(account)
                                       data=cur.fetchall()
                                       ID=data[0][0]
                                       for row in data:
                                             print('   Student ID    : ',row[0])
                                             print('     Name        : ',row[1].capitalize())
                                             print('stream/department: ',row[2].capitalize())
                                       else:
                                           print()
                                           alter=input('change username/password yes/no: ').lower()
                                           if alter=='yes':            
                                                   username_verification=input('Old username: ')
                                                   password_verification=input('Old password: ')              
                                                   if username_verification==username and password_verification==password:
                                                       new_username=input('New username: ')
                                                       new_password=input('New password: ')
                                                       confirm_username=input('Confirm username: ')
                                                       confirm_password=input('Confirm password: ')
                                                       if new_username=='' or new_password=='':
                                                             print('username/password cannot be empty')
                                                             continue
                                                       elif new_username==confirm_username and new_password==confirm_password:
                                                           update='''update members
                                                                     set username='{}',password='{}'
                                                                     where id='{}';'''.format(new_username,new_password,ID)
                                                           cur.execute(update)
                                                           con.commit()
                                                           print('Successfully changed username and password')
                                                           continue
                                                       else:
                                                           print()
                                                           print('username/password confirmation does not match')
                                                           
                                                   else:
                                                        print('username/password does not match')
                                           elif alter=='no':
                                                 continue
                                           else:
                                                print('Invalid choice. Try again')
                                   elif choice==5:
                                       file=open('rules and regulations student.txt','r')
                                       s=file.read()
                                       print(s)
                                       print()
                                       input('press enter to go to main menu')
                                   elif choice==6:
                                       print('''
                            ------------------------------------------------
                                     SUGGESTIONS AND COMPLAINTS
                            ------------------------------------------------''')
                                       from datetime import date                              
                                       date=date.today()
                                       n='''select * from complaints; '''
                                       cur.execute(n)
                                       data=cur.fetchall()
                                       sno_count=cur.rowcount
                                       sno=sno_count+1
                                       s=input('suggestion/complaint: ')
                                       cmd='''insert into complaints(sno,date,complaint)
                                              values({},'{}','{}')'''.format(sno,date,s)
                                       cur.execute(cmd)
                                       con.commit()
                                   elif choice==7:
                                         break
                                   else:
                                       print('Invalid choice. Try again')
                         else:
                              print('username and password does not match')
                             
              if login_as==2:
                    sql_connection()
                    username=input('Username: ')
                    user_search='''select * from members
                                   where username='{}' and id like 'TE%';'''.format(username)
                    cur.execute(user_search)
                    data=cur.fetchall()
                    n=cur.rowcount
                    if n==0:
                          print('username does not exist')
                    else:
                         password=input('Password: ')
                         passwd_search='''select password from members
                                          where username='{}';'''.format(username)
                         cur.execute(passwd_search)
                         data=cur.fetchall()
                         if password==data[0][0]:
                             while True:
                                   menu='''
                                        
                                                             MENU
                                        --------------------------------------------------
                                             1.Books
                                             2.My books
                                             3.My account
                                             4.Fines
                                             5.Rules and regulations
                                             6.Suggestions and complaints
                                             7.sign out
                                             '''
                                   print(menu)
                                   choice=int(input('select your choice: '))
                                   if choice==1:
                                         menu='''
                                        --------------------------------------------------
                                                            Books
                                        --------------------------------------------------
                                                  1.Display all books
                                                  2.Search
                                                   '''
                                         print(menu)
                                         choice=int(input('select your choice: '))
                                         if choice==1:
                                               sql_connection()
                                               books='''select bookno,bookname,author,genre,version,publication,location from books;'''
                                               cur.execute(books)
                                               data=cur.fetchall()
                                               table='''
+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+
|Bookno    |Book name                |Author           |genre            |version   |publication    |location |
+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+'''
                                               d='''|%10s|%25s|%17s|%17s|%10s|%15s|%9s|'''

                                               print(table)
                                               for row in data:
                                                     print(d%(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
                                               else:
                                                       print('''+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+''')
                                                       print()
                                                       print()
                                                       input('press enter to go to main menu')
                                         elif choice==2:
                                               booksearch()
                                               print()
                                               print()
                                               input('press enter to go to main menu')
                                         else:
                                               print('wrong choice')
                                   elif choice==2:
                                       print('''
                                        --------------------------------------------------
                                                            MY BOOKS
                                        --------------------------------------------------''')
                                       print()
                                       account='''select id from members
                                                  where username='{}'and password='{}';'''.format(username,password)

                                       cur.execute(account)
                                       data=cur.fetchall()
                                       ID=data[0][0]
                                       books='''select bookno,bookname,author,genre,version,publication,location,dateborrowed from books where borrowedby='{}';'''.format(ID)
                                       cur.execute(books)
                                       data=cur.fetchall()
                                       table='''
+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+-------------+
|Bookno    |Book name                |Author           |genre            |version   |publication    |location |dateborrowed |
+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+-------------+'''
                                       d='''|%10s|%25s|%17s|%17s|%10s|%15s|%9s|%13s|'''
                                       print(table)
                                       for row in data:
                                             print(d%(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
                                       else:
                                            print('''+----------+-------------------------+-----------------+-----------------+----------+---------------+---------+-------------+''')
                                            print()
                                            print()
                                            input('press enter to go to main menu')
                                   elif choice==3:
                                       print('''
                                        --------------------------------------------------
                                                            MY ACCOUNT
                                        --------------------------------------------------''')

                                       account='''select id,name,streamdepartment from members
                                                  where username='{}'and password='{}';'''.format(username,password)

                                       cur.execute(account)
                                       data=cur.fetchall()
                                       ID=data[0][0]
                                       for row in data:
                                             print('   Student ID    : ',row[0])
                                             print('     Name        : ',row[1].capitalize())
                                             print('stream/department: ',row[2].capitalize())
                                       else:
                                           print()
                                           alter=input('change username/password yes/no: ').lower()
                                           if alter=='yes':            
                                                   username_verification=input('Old username: ')
                                                   password_verification=input('Old password: ')              
                                                   if username_verification==username and password_verification==password:
                                                       new_username=input('New username: ')
                                                       new_password=input('New password: ')
                                                       confirm_username=input('Confirm username: ')
                                                       confirm_password=input('Confirm password: ')
                                                       if new_username=='' or new_password=='':
                                                             print('username/password cannot be empty')
                                                             continue
                                                       elif new_username==confirm_username and new_password==confirm_password:
                                                           update='''update members
                                                                     set username='{}',password='{}'
                                                                     where id='{}';'''.format(new_username,new_password,ID)
                                                           cur.execute(update)
                                                           con.commit()
                                                           print('Successfully changed username and password')
                                                           continue
                                                       else:
                                                           print()
                                                           print('username/password confirmation does not match')
                                                           
                                                   else:
                                                        print('username/password does not match')
                                           elif alter=='no':
                                                 continue
                                           else:
                                                print('Invalid choice. Try again')
                                   elif choice==4:
                                       fine_read()
                                       print(''' 
                                        --------------------------------------------------
                                                            FINES
                                        --------------------------------------------------''')
                                       print()
                                       account='''select id from members
                                                  where username='{}'and password='{}';'''.format(username,password)
                                       cur.execute(account)
                                       d=cur.fetchall()
                                       ID=d[0][0]
                                       qs='''select bookno,bookname,dateborrowed,fine from books
                                             where borrowedby='{}';'''.format(ID)
                                       cur.execute(qs)
                                       data=cur.fetchall()
                                       table='''
+--------+----------------------------+-------------+-------+
|Bookno  |Book name                   |Date borrowed| Fines |
+--------+----------------------------+-------------+-------+'''
                                       print(table)
                                       d='''|%8s|%28s|%13s|%7s|'''
                                       amount=0    
                                       for row in data:
                                           print(d%(row[0],row[1],row[2],row[3]))
                                           amount+=row[3]
                                       else:
                                           print('+--------+----------------------------+-------------+-------+')
                                           print()
                                           print('Total fine payable: ',amount)
                                           print()
                                           input('Press enter to continue')
                                           
                                   elif choice==5:
                                       file=open('rules and regulations teacher.txt','r')
                                       s=file.read()
                                       print(s)
                                       print()
                                       input('press enter to go to main menu')
                                   elif choice==6:
                                       print('''
                            ------------------------------------------------
                                     SUGGESTIONS AND COMPLAINTS
                            ------------------------------------------------''')
                                       from datetime import date                              
                                       date=date.today()
                                       n='''select * from complaints; '''
                                       cur.execute(n)
                                       data=cur.fetchall()
                                       sno_count=cur.rowcount
                                       sno=sno_count+1
                                       s=input('suggestion/complaint: ')
                                       cmd='''insert into complaints(sno,date,complaint)
                                              values({},'{}','{}')'''.format(sno,date,s)
                                       cur.execute(cmd)
                                       con.commit()
                                   elif choice==7:
                                       break
                                   else:
                                        print('Invalid choice. Try again')
                         else:
                              print('username and password does not match')
              elif login_as==3:
                    sql_connection()
                    username=input('Username: ')
                    user_search='''select * from members
                                   where username='{}' and id like 'AD%';'''.format(username)

                    cur.execute(user_search)
                    data=cur.fetchall()
                    n=cur.rowcount
                    if n==0:
                          print('username does not exist')
                    else:
                         password=input('Password: ')
                         passwd_search='''select password from members
                                          where username='{}';'''.format(username)
                         cur.execute(passwd_search)
                         data=cur.fetchall()
                         if password==data[0][0]:
                             while True:
                                   menu='''
                                        
                                                            MAIN MENU
                                        --------------------------------------------------
                                             1.Books
                                             2.Members
                                             3.Accounts
                                             4.Create new admin account
                                             5.Sign out
                                             '''
                                   print(menu)
                                   choice=int(input('select your choice: '))
                                   if choice==1:
                                      while True:
                                           menu='''
                                        --------------------------------------------------
                                                            Books
                                        --------------------------------------------------
                                                  1.List of books in library
                                                  2.Search books
                                                  3.Book in use
                                                  4.Add new books
                                                  5.Delete books
                                                  6.Add books borrowed by members
                                                  7.Go back to main menu
                                                   '''
                                           print(menu) 
                                           choice=int(input('select your choice: '))
                                           if choice==1:

                                               print('''
                                        --------------------------------------------------
                                                   LIST OF BOOKS IN LIBRARY 
                                        --------------------------------------------------''')
                                               sql_connection()
                                               books='''select bookno,bookname,author,genre,version,publication,location,availability,borrowedby,dateborrowed from books;'''
                                               cur.execute(books)
                                               data=cur.fetchall()
                                               table='''
+--------+-------------------------+----------------+-----------------+-------+---------------+--------+-------------+-----------+-------------+
|Bookno  |Book name                |Author          |genre            |version|publication    |location|availability |borrowedby |dateborrowed |
+--------+-------------------------+----------------+-----------------+-------+---------------+--------+-------------+-----------+-------------+'''
                                               d='''|%8s|%25s|%16s|%17s|%7s|%15s|%8s|%13s|%11s|%13s|'''
                                               print(table)
                                               for row in data:
                                                     print(d%(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
                                               else:
                                                    print('''+--------+-------------------------+----------------+-----------------+-------+---------------+--------+-------------+-----------+-------------+''')
                                                    print()
                                                    print()
                                                    input('press enter to go back to main menu')
                                           elif choice==2:
                                                 booksearch()
                                                 print()
                                                 print()
                                                 input('press enter to go back to books')  
                                           elif choice==3:
                                                                                          
                                               print('''
                                        --------------------------------------------------
                                                         BOOKS IN USE
                                        --------------------------------------------------''')
                                               books_in_use()
                                               print()
                                               input('press enter to go back to books')
                                           elif choice==4:
                                               print('''
                                        --------------------------------------------------
                                                         ADD NEW BOOKS
                                        --------------------------------------------------''')
                                               add_new_books()
                                               print()
                                               print('Added new book')
                                           elif choice==5:
                                               print('''
                                        --------------------------------------------------
                                                         DELETE BOOKS
                                        --------------------------------------------------''')
                                               delete_books()
                                           elif choice==6:
                                               print('''
                                        --------------------------------------------------
                                                ADD BOOKS BORROWED BY MEMBERS
                                        --------------------------------------------------''')
                                               bookno=int(input('Enter bookno of book borrowed by member: '))
                                               st1='''select * from books where bookno='{}';'''.format(bookno)
                                               cur.execute(st1)
                                               cur.fetchall()
                                               n=cur.rowcount
                                               if n==0:
                                                    print('The bookno does not exist')
                                               else:
                                                     sql_connection()
                                                     from datetime import date
                                                     date=date.today()
                                                     print("first three characters of id should be in this format, 'ST/'  for students,'TE/' for teachers,'AD/' for admin") 
                                                     ID=input('Input id of member borrowing book: ')
                                                     st='''select * from members where id='{}'; '''.format(ID)
                                                     cur.execute(st)
                                                     cur.fetchall()
                                                     data=cur.rowcount
                                                     if data==0:
                                                           print('given id does not exist')
                                                     else:
                                                           sql_connection()
                                                           st2='''update books set availability='no' where bookno='{}'; '''.format(bookno)
                                                           st3='''update books set borrowedby='{}' where bookno='{}'; '''.format(ID,bookno)
                                                           st4='''update books set dateborrowed='{}' where bookno='{}'; '''.format(date,bookno)
                                                           cur.execute(st2)
                                                           cur.execute(st3)
                                                           cur.execute(st4)
                                                           con.commit()
                                                           print('request done')
                                           
                                           elif choice==7:
                                               break    
                                           else:
                                               print('Invalid choice. Try again')
                                   elif choice==2:
                                        menu_user='''
                                                               USER
                                                  -------------------------------
                                                    1.List of members
                                                    2.Delete members
                                                    3.List of suggestions/complaints
                                                    4.User activity
                                                    5.Go back to last menu
                                                                                            '''
                                        while True:
                                              print(menu_user)
                                              choice=int(input('enter a choice: '))
                                              if choice==1:
                                                  print('''
                                        --------------------------------------------------
                                                         LIBRARY MEMBERS
                                        --------------------------------------------------''')
                                                  members()
                                                  print()
                                                  input('press enter to continue')
                                              elif choice==2:
                                                  print('''
                                        --------------------------------------------------
                                                         DELETE MEMBER
                                        --------------------------------------------------''')
                                                  del_members()
                                              elif choice==3:
                                                  print('''
                                        --------------------------------------------------
                                                  LIST OF SUGGESTIONS/COMPLAINTS
                                        --------------------------------------------------''')
                                                  complaint()
                                                  print()
                                                  input('press enter to continue')
                                              elif choice==4:
                                                  print('''
                                        --------------------------------------------------
                                                        USER ACTIVITY
                                        --------------------------------------------------''')
                                                  user_activity()
                                                  print()
                                                  input('press enter to continue')
                                              elif choice==5:
                                                  break
                                              else:
                                                  print('Invalid choice. Try again')
                                   elif choice==3:
                                       while True:
                                           menu='''
                                                          ACCOUNTS  
                                        ---------------------------------------------------
                                           1.Fines
                                           2.Transactions
                                           3.Today's payments 
                                           4.All payments
                                           5.Go back to last menu'''
                                           print(menu)
                                           choice=int(input('Enter your choice: '))
                                           fine_read()
                                           if choice==1:
                                               fine_read()
                                               print('''
                                        --------------------------------------------------
                                                           FINES
                                        --------------------------------------------------''')
                                               print()
                                               qs='''select bookno,bookname,dateborrowed,borrowedby,fine from books where availability='no';'''
                                               cur.execute(qs)
                                               data=cur.fetchall()
                                               table='''
+--------+----------------------------+-------------+------------+-------+
|Bookno  |Book name                   |Date borrowed|Borrowed by | Fines |
+--------+----------------------------+-------------+------------+-------+'''
                                               print(table)
                                               d='''|%8s|%28s|%13s|%12s|%7s|'''
                                               for row in data:
                                                   print(d%(row[0],row[1],row[2],row[3],row[4]))
                                               else:
                                                   print('+--------+----------------------------+-------------+------------+-------+')
                                                   print()
                                                   input('Press enter to continue') 
                                           elif choice==2:
                                               print('''
                                        --------------------------------------------------
                                                        TRANSACTIONS
                                        --------------------------------------------------''')
                                               transactions()
                                           elif choice==3:
                                                from datetime import date
                                                date=date.today()
                                                qs='''select * from payments where date='{}';'''.format(date)
                                                cur.execute(qs)
                                                data=cur.fetchall()
                                                if data==[]:
                                                      print('There is no payments')
                                                else:
                                                      table='''
+-----+------------+------------+------------+
|S.no |Date        |ID          |Amount      |
+-----+------------+------------+------------+'''
                                                      print(table)
                                                      d='''|%5s|%12s|%12s|%12s|'''
                                                      amount=0
                                                      for row in data:
                                                            print(d%(row[0],row[1],row[2],row[3]))
                                                            amount+=row[3]
                                                      else:
                                                            print('+-----+------------+------------+------------+')
                                                            print()
                                                            print("Today's closing amount: ",amount)
                                                            print()
                                                            input('Press enter to continue')

                                           elif choice==4:
                                                print('''
                                        --------------------------------------------------
                                                         ALL PAYMENTS 
                                        --------------------------------------------------''')
                                                qs='''select * from payments'''
                                                cur.execute(qs)
                                                data=cur.fetchall()
                                                if data==[]:
                                                      print('There is no payments')
                                                else:
                                                      table='''
+-----+------------+------------+------------+
|S.no |Date        |ID          |Amount      |
+-----+------------+------------+------------+'''
                                                      print(table)
                                                      d='''|%5s|%12s|%12s|%12s|'''
                                                      for row in data:
                                                            print(d%(row[0],row[1],row[2],row[3]))
                                                      else:
                                                            print('+-----+------------+------------+------------+')
                                                            print()
                                                            input('Press enter to continue')
                                                            
                                           else:
                                               break        
                                   elif choice==4:
                                          ID=input('ID starting with AD/: ').upper()
                                          if 'AD/' in ID:
                                              name=input('Full name: ').lower()
                                              stream=input('Stream/department: ').lower()
                                              username=input('Username: ')
                                              c_username=input('Confirm username: ')
                                              if username==c_username:
                                                  password=input('Password: ')
                                                  c_password=input('Confirm password: ')
                                                  if password==c_password:
                                                      file=open('rules and regulations teacher.txt','r')
                                                      s=file.read()
                                                      print(s)
                                                      print()
                                                      c=input('Agree rules and regulations y/n: ').lower()
                                                      if c=='y':
                                                          sql_connection()
                                                          qs='''insert into members(id,name,username,password,streamdepartment)
                                                                values('{}','{}','{}','{}','{}');'''.format(ID,name,username,password,stream)
                                                          cur.execute(qs)
                                                          con.commit()
                                                          print()
                                                          print('Successfully created new account')
                                                          print('          DETAILS')
                                                          print('   Student ID    : ',ID)
                                                          print('     Name        : ',name)
                                                          print('Stream/department: ',stream)
                                                          print('   Username      : ',username)
                                                          print('   Password      : ',password)
                                                          print()
                                                          input('Press enter to continue')
                                                                                  
                                                  else:
                                                      print('Password confirmation does not match')
                                              else:
                                                  print('Username confirmation does not match')                   
                                          else:
                                              print('Wrong ID format')
                                   elif choice==5:
                                       break
              elif login_as==4:
                  while True:
                          menu='''
                                                --------------------------------------------------
                                                                CREATE NEW ACCOUNT
                                                --------------------------------------------------
                                                       1.Student
                                                       2.Teacher
                                                       3.Go back to last menu
                                                       '''
                          print(menu)
                          choice=int(input('Enter your choice: '))
                          if choice==1:
                              ID=input('ID starting with ST/: ').upper()
                              if 'ST/' in ID:
                                  name=input('Full name: ').lower()
                                  stream=input('Stream/department: ').lower()
                                  username=input('Username: ')
                                  c_username=input('Confirm username: ')
                                  if username==c_username:
                                      password=input('Password: ')
                                      c_password=input('Confirm password: ')
                                      if password==c_password:
                                          file=open('rules and regulations student.txt','r')
                                          s=file.read()
                                          print(s)
                                          print()
                                          c=input('Agree rules and regulations y/n: ').lower()
                                          if c=='y':
                                              sql_connection()
                                              qs='''insert into members(id,name,username,password,streamdepartment)
                                                    values('{}','{}','{}','{}','{}');'''.format(ID,name,username,password,stream)
                                              cur.execute(qs)
                                              con.commit()
                                              print()
                                              print('Successfully created new account')
                                              print('          DETAILS')
                                              print('   Student ID    : ',ID)
                                              print('     Name        : ',name)
                                              print('Stream/department: ',stream)
                                              print('   Username      : ',username)
                                              print('   Password      : ',password)
                                              print()
                                              input('Press enter to continue')
                                      
                                      else:
                                          print('Password confirmation does not match')
                                  else:
                                      print('Username confirmation does not match')
                              else:
                                  print('Wrong ID format')
                          elif choice==2:
                              ID=input('ID starting with TE/: ').upper()
                              if 'TE/' in ID:
                                  name=input('Full name: ').lower()
                                  stream=input('Stream/department: ').lower()
                                  username=input('Username: ')
                                  c_username=input('Confirm username: ')
                                  if username==c_username:
                                      password=input('Password: ')
                                      c_password=input('Confirm password: ')
                                      if password==c_password:
                                          file=open('rules and regulations teacher.txt','r')
                                          s=file.read()
                                          print(s)
                                          print()
                                          c=input('Agree rules and regulations y/n: ').lower()
                                          if c=='y':
                                              sql_connection()
                                              qs='''insert into members(id,name,username,password,streamdepartment)
                                                    values('{}','{}','{}','{}','{}');'''.format(ID,name,username,password,stream)
                                              cur.execute(qs)
                                              con.commit()
                                              print()
                                              print('Successfully created new account')
                                              print('          DETAILS')
                                              print('   Student ID    : ',ID)
                                              print('     Name        : ',name)
                                              print('Stream/department: ',stream)
                                              print('   Username      : ',username)
                                              print('   Password      : ',password)
                                              print()
                                              input('Press enter to continue')
                                      else:
                                          print('Password confirmation does not match')
                                  else:
                                      print('Username confirmation does not match')
                              else:
                                  print('Wrong ID format')
                          elif choice==3:
                                    break
                          else:
                              print('Wrong choice. Try again')
            
except ValueError:
    print()
    print('#ERROR')
    print("Un necessarily pressing 'ENTER' keys can crash program ")

