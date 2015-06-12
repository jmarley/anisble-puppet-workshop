class install_eap6 {

  file { '/opt/myrepo/': ensure => directory }

  file { '/opt/myrepo/jboss-eap-6.4-1.0-1.el7.x86_64.rpm':
    ensure => "file",
    source => "puppet:///modules/eap-6-cfg/rpm/jboss-eap-6.4-1.0-1.el7.x86_64.rpm",
  }

  file { '/opt/myrepo/jboss-repo.repo':
    ensure => "file",
    source => "puppet:///modules/eap-6-cfg/data/jboss-repo.repo",
  }
}
