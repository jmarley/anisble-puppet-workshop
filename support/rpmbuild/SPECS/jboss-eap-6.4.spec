Name: jboss-eap-6.4           
Version: 1.0        
Release:        1%{?dist}
Summary: Wrapping EAP zip in distributable package 

Group: System Environment/Base
License: GPLv2+       
URL: http://www.irs.gov 
         
Source0: jboss-eap-6.4.0.zip       
Source1: jbosseap6.service       

# jboss home variable
%define jboss_version jboss-eap-6.4
%define jboss_home /opt/jboss/%{jboss_version}
%define user jboss

Requires: java-1.7.0-openjdk
Requires: unzip

%description
This rpm takes the EAP package from Red Hat in zip format and packages into an 
rpm which is then installed in locations defined in spec.


%prep
             	
unzip %SOURCE0

%build
#Not in use

%install
rm -rf $RPM_BUILD_ROOT

# Create initd Start/Stop directory
#install -d $RPM_BUILD_ROOT/etc/jboss-as

# Create log directory
#install -d $RPM_BUILD_ROOT/var/log/jboss-as

# Create SSL directory
install -d -m 0755 $RPM_BUILD_ROOT/opt/jboss/vault 

# Create run directory
install -d $RPM_BUILD_ROOT/var/run/jboss-as

install -d -m 0755 $RPM_BUILD_ROOT/opt/jboss

# Add EAP systemctl service file

cp %SOURCE1 ./%{jboss_version}/bin/init.d

# Add EAP to package
cp -r ./%{jboss_version} $RPM_BUILD_ROOT/opt/jboss

# Make log and data dir's
install -d -m 2750 $RPM_BUILD_ROOT%{jboss_home}/standalone/log
install -d -m 2750 $RPM_BUILD_ROOT%{jboss_home}/standalone/data

%clean
rm -rf $RPM_BUILD_ROOT


%files
#change the directory owner/group
%defattr(-,jboss,jboss,-)

# Add JBoss directory and contents to RPM
%config(noreplace)/opt/jboss

# Add SSL directory to RPM
%config(noreplace)/opt/jboss/vault

#Adjust permissions
#%config(noreplace)%attr(2755, JbossAdm,JbossAdm) /etc/jboss-as
#%config(noreplace)%attr(2775, jboss,jboss) /var/run/jboss-as
#%config(noreplace)%attr(2775, jboss,jboss) /var/log/jboss-as

%pre

getent passwd %{user} > /dev/null 2&>1

if [ $? -ne 0 ]; then
	useradd -M -s /sbin/nologin -c 'jboss process owener' %{user}
fi

%post
# Runs after the install

# Configure jboss-as.conf
echo 'JBOSS_CONSOLE_LOG=/dev/null' >> %{jboss_home}/bin/init.d/jboss-as.conf
echo 'JBOSS_USER=jboss' >> %{jboss_home}/bin/init.d/jboss-as.conf
echo "JBOSS_CONFIG='"'standalone.xml -Djboss.bind.address=$HOSTNAME'"'" >> %{jboss_home}/bin/init.d/jboss-as.conf
echo 'JBOSSCONF=standalone'  >> %{jboss_home}/bin/init.d/jboss-as.conf
echo 'JBOSS_HOME='%{jboss_home}  >> %{jboss_home}/bin/init.d/jboss-as.conf

mkdir /etc/jboss-as
cp %{jboss_home}/bin/init.d/jboss-as.conf /etc/jboss-as/
cp %{jboss_home}/bin/init.d/jboss-as-standalone.sh /etc/init.d/jboss-standalone.sh

# Initialize Startup Script 
#cp %{jboss_home}/bin/init.d/jbosseap6.service /etc/systemd/system/
#systemctl enable jbosseap6

# Initialize Startup Script
#ln -s %{jboss_home}/bin/init.d/jboss-as.conf /etc/jboss-as/
#ln -s %{jboss_home}/bin/init.d/jboss-as-standalone.sh /etc/init.d/jboss-standalone.sh

chkconfig --add jboss-standalone.sh


%preun
# This stanza runs when the package is removed via yum 
# Stop server
#systemctl stop jbosseap6
service jboss-standalone stop

# Wait for it
sleep 10


#systemctl disable jbosseap6

#remove jboss process owner
userdel jboss

chkconfig --del jboss-standalone 

# Remove EAP
/bin/rm -rf %{jboss_home}/

/bin/rm -rf /var/log/jboss-as/

/bin/rm -rf /var/run/jboss-as/

/bin/rm -rf /etc/jboss-as

exit 0

%changelog


