
### Lab Description

This lab contains a [blind SQL injection](https://portswigger.net/web-security/sql-injection/blind) vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows. If the SQL query causes an error, then the application returns a custom error message.

The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind [SQL injection](https://portswigger.net/web-security/sql-injection) vulnerability to find out the password of the `administrator` user.

#### Hint

> This lab uses an Oracle database. For more information, see the [SQL injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet).


#### Lab solution

- 1. Trigger error ( ' single quote at cookie)
![[Pasted image 20230529183051.png]]
![[Pasted image 20230529183117.png]]

- 2. Oracle database ( this will trigger an error because Oracle always required a from dual at the end of a command)
![[Pasted image 20230529183623.png]]
![[Pasted image 20230529183724.png]]

- 3. ow that you've crafted what appears to be a valid query, try submitting an invalid query while still preserving valid SQL syntax. For example, try querying a non-existent table name:
```sql
TrackingId=xyz'||(SELECT '' FROM not-a-real-table)||'
```
- 4. Trigger the SQL true condition
![[Pasted image 20230529184138.png]]

- 5. Enumerate user `administrator` ( if the error returned if enumerate user, otherwise the user not exists)
![[Pasted image 20230529184303.png]]

- 6. how many characters are in the password of the `administrator`
![[Pasted image 20230529184516.png]]
- 7. The next step is to test the character at each position to determine its value
`'||(SELECT CASE WHEN SUBSTR(password,20,1)='b' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'`

![[Pasted image 20230529185110.png]]

- Lab Solved!