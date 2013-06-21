##############################################################
##
## Powershell Active Directory User Tally
##
## For use in reporting how many AD users we have every month
## Bill Moylan
##############################################################

 function sendMail{

     #Creating a Mail object
     $msg = new-object Net.Mail.MailMessage

     #Creating SMTP server object
     $smtp = new-object Net.Mail.SmtpClient("webmail.graisellsworth.com")

     #Email structure 
     $msg.From = "adReporter@graisellsworth.com"
     $msg.ReplyTo = "wmoylan@graisellsworth.com"
     $msg.To.Add("wmoylan@graisellsworth.com", "talberi@graisellsworth.com")#, "Lis.Mote@mindshift.com")
     $msg.subject = "AD Count"
     $msg.body = "The curent number of Grais & Ellsworth Active Directory users is: " + ($count.count + $Vendors)

     #Sending email 
     $smtp.Send($msg)
  
}
#Fetch the count of users from AD
cd "AD:\OU=Users,OU=Production,OU=GE,DC=GE, DC=local"
$count = dir
$count.count

#Add the number in VendorAdjust.txt
$vendors = get-content C:\Users\billadmin\Documents\VendorAdjust.txt

sendmail

