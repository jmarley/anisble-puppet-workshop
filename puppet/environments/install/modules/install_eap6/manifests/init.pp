class install_eap6 {

  package { "vim-enhanced":  ensure => present}

  package { "createrepo":  ensure => present }

  package { "yum-utils":  ensure => present }


  notify { "installing eap": }->
  package { "jboss-eap-6.4":  
    ensure  => present,
    require => Exec["add_jboss_repo_to_yum"],
  }->
  notify { "eap installed": }

  notify { "creating myrepo dir": }-> 
  file { '/opt/myrepo/': 
    ensure => directory, 
  }->
  notify { "myrepo dir created": } 

  notify { "copying rpm": }->
  file { '/opt/myrepo/jboss-eap-6.4-1.0-1.el7.x86_64.rpm':
    ensure  => "file",
    source  => "puppet:///modules/install_eap6/rpm/jboss-eap-6.4-1.0-1.el7.x86_64.rpm",
    require => File["/opt/myrepo"],
  }->
  notify { "rpm copied": }

  notify { "copying repo": }->
  file { '/opt/myrepo/jboss-repo.repo':
    ensure  => "file",
    source  => "puppet:///modules/install_eap6/data/jboss-repo.repo",
    require => File["/opt/myrepo"],
  }->
  notify { "repo added": message => "myrepo dir added", } 
  
  notify { "copying war": }->
  file { '/opt/jboss/jboss-eap-6.4/standalone/deployments/jboss-helloworld-puppet.war':
    ensure  => "file",
    source  => "puppet:///modules/install_eap6/bin/jboss-helloworld-puppet.war",
    require => Package["jboss-eap-6.4"],
  }->
  notify { 'war copied': message => "jboss war was successfully copied", }

  notify { "creating yum repo": }->
# create yum repo
  exec { "create_yum_repository":
    command => "/usr/bin/createrepo --database /opt/myrepo",
    require => [ Package["createrepo"], 
                 File["/opt/myrepo/jboss-repo.repo"], 
                 File["/opt/myrepo/jboss-eap-6.4-1.0-1.el7.x86_64.rpm"]
                 ],
  }->
  notify { "repository created": }

  notify { "adding repo to yum": }->
# add new repo to yum
  exec { "add_jboss_repo_to_yum":
    command => "/usr/bin/yum-config-manager --add-repo /opt/myrepo/jboss-repo.repo --enable",
    require => [ Package["yum-utils"],
                 Exec["create_yum_repository"]
               ],
  }->
  notify { "repo managed yum": }

# add new repo to yum part duex
#  yumrepo { "add_jboss_repo_to_yum":
#    baseurl  => "file:///opt/myrepo/jboss-repo.repo",
#    descr    => "EAP 6 repository",
#    enabled  => 1,
#    gpgcheck => 0,
#  }

# deploy hellow world app

  notify { "starting eap as a service": }->
# start eap yum
  service { "jboss-eap-6.4":
    ensure  => "running",
    require => Package["jboss-eap-6.4"],
  }->
  notify { "eap service started": }

}
