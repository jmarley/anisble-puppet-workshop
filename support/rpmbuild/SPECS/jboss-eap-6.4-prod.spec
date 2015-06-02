Name: jboss-eap-6.4           
Version: 1.0        
Release:        1%{?dist}
Summary: Wrapping EAP zip in distributable package 

Group: System Environment/Base
License: GPLv2+       
URL: http://www.irs.gov 
         
Source0: jboss-eap-6.4.0.tar.gz       

# jboss home variable
%define jboss_version jboss-eap-6.4
%define jboss_home /opt/jboss/%{jboss_version}

Requires: java-1.7.0-openjdk

%description
This rpm takes the EAP package from Red Hat in zip format and packages into an 
rpm which is then installed in locations defined in spec.


%prep
%setup -q -c 

%build
#Not in use

%install
rm -rf $RPM_BUILD_ROOT

# Create initd Start/Stop directory 
install -d $RPM_BUILD_ROOT/etc/jboss-as

# Create log directory
install -d $RPM_BUILD_ROOT/var/log/jboss-as

# Create run directory
install -d $RPM_BUILD_ROOT/var/run/jboss-as

# Create SSL directory
install -d -m 0755 $RPM_BUILD_ROOT/opt/jboss/vault 

# Create EAP directory
install -d -m 0755 $RPM_BUILD_ROOT/opt/jboss

# Add EAP to package
cp -r ./%{jboss_version} $RPM_BUILD_ROOT/opt/jboss

# Make log and data dir's
install -d -m 2750 $RPM_BUILD_ROOT%{jboss_home}/standalone/log
install -d -m 2750 $RPM_BUILD_ROOT%{jboss_home}/standalone/data

# Add Microsoft Data Source (can customize more)
cp -r ./mymodules $RPM_BUILD_ROOT/opt/jboss/mymodules

# security
# Add Vault to EAP
cp -r ./keystores/vault.keystore $RPM_BUILD_ROOT/opt/jboss/vault
cp -r ./keystores/VAULT.dat $RPM_BUILD_ROOT/opt/jboss/vault

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
%config(noreplace)%attr(2755, jboss,jboss) /etc/jboss-as
%config(noreplace)%attr(2755, jboss,jboss) /var/log/jboss-as
%config(noreplace)%attr(2775, jboss,jboss) /var/run/jboss-as


%pre
# Not in use
useradd -M -s /sbin/nologin -c 'jboss process owener' jboss


%post
# Runs after the install

# Configure jboss-as.conf
echo 'JBOSS_CONSOLE_LOG=/dev/null' >> ${jboss_home}/bin/init.d/jboss-as.conf
echo 'JBOSS_USER=jboss' >> ${jboss_home}/bin/init.d/jboss-as.conf
echo "JBOSS_CONFIG='"'standalone.xml -Djboss.bind.address=$HOSTNAME'"'" >> ${jboss_home}/bin/init.d/jboss-as.conf
echo 'JBOSSCONF=standalone'  >> ${jboss_home}/bin/init.d/jboss-as.conf
echo 'JBOSS_HOME='${jboss_home}  >> ${jboss_home}/bin/init.d/jboss-as.conf

# Initialize Startup Script
ln -s ${jboss_home}/bin/init.d/jboss-as.conf /etc/jboss-as/
ln -s ${jboss_home}/bin/init.d/jboss-as-standalone.sh /etc/init.d/jboss-as

chkconfig --add jboss-as

%preun
# This stanza runs when the package is removed via yum 
# Stop server
service jboss-as stop

# Wait for it
sleep 10

chkconfig --del jboss-as

#remove jboss process owner
userdel jboss

/bin/unlink /etc/init.d/jboss-as.conf
/bin/unlink /etc/init.d/jboss-as

# Remove EAP
/bin/rm -rf %{jboss_home}/

/bin/rm -rf /etc/init.d/jboss-as

/bin/rm -rf /var/log/jboss-as/

/bin/rm -rf /var/run/jboss-as/

/bin/rm -rf /etc/jboss-as

exit 0

%changelog


