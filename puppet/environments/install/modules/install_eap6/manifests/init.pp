class install_eap6 {

  package { createrepo:  ensure => present }

  package { yum-utils:  ensure => present }

  package { jboss-eap-6.4:  ensure => present }

  file { '/opt/myrepo/': ensure => directory }
 
  notify { 'myrepo dir added': }
 
  file { '/opt/myrepo/jboss-eap-6.4-1.0-1.el7.x86_64.rpm':
    ensure => "file",
    source => "puppet:///modules/eap-6-cfg/rpm/jboss-eap-6.4-1.0-1.el7.x86_64.rpm",
  }

  file { '/opt/myrepo/jboss-repo.repo':
    ensure => "file",
    source => "puppet:///modules/eap-6-cfg/data/jboss-repo.repo",
  }

# create yum repo

# add new repo to yum

# install jboss eap

# deploy hellow world app

# start eap yum

}
