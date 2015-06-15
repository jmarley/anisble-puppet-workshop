class install_eap6 {

  package { "createrepo":  ensure => present }

  package { "yum-utils":  ensure => present }

  package { "jboss-eap-6.4":  
    ensure  => present,
    require => Exec["add_jboss_repo_to_yum"]}

  file { '/opt/myrepo/': ensure => directory }
 
  notify { 'myrepo dir added': }
 
  file { '/opt/myrepo/jboss-eap-6.4-1.0-1.el7.x86_64.rpm':
    ensure => "file",
    source => "puppet:///modules/install_eap6/rpm/jboss-eap-6.4-1.0-1.el7.x86_64.rpm",
  }

  file { '/opt/myrepo/jboss-repo.repo':
    ensure => "file",
    source => "puppet:///modules/install_eap6/data/jboss-repo.repo",
  }
  
  file { '/opt/jboss/jboss-eap-6.4/standalone/deployments/ ':
    ensure  => "file",
    source  => "puppet:///modules/install_eap6/bin",
    require => Package["jboss-eap-6.4"],
  }

# create yum repo
  exec { "create_yum_repository":
    command => "/usr/bin/createrepo --database /opt/myrepo",
    require => Package["createrepo"], 
  }
 
# add new repo to yum
  exec { "add_jboss_repo_to_yum":
    command => "/usr/bin/yum-config-manager --add-repo /opt/myrepo/jboss-repo.repo --enable",
    require => Package["yum-utils"],
  }

# deploy hellow world app
 

# start eap yum
  service { "jboss-eap-6.4":
    ensure => "running",
  }
}
