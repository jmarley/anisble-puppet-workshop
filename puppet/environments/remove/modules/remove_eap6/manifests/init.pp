class remove_eap6 {

  notify { "removing rpm": }->
  package { "jboss-eap-6.4":
    ensure  => absent,
    require => Service[ "jboss-eap-6.4" ],
  }->
  notify { "rpm removed": }

  notify { "starting to remove repo dir": }->
  file { '/opt/myrepo/':
    path    => '/opt/myrepo/',
    ensure  => absent, 
    recurse => true,
    purge   => true,
    force   => true,
    require => Exec["disable_jboss_repo_from_yum"], 
  }->
  notify { "myrepo dir removed": }

  notify { "disabling jboss repo dir": }->
# remove new repo to yum
  exec { "disable_jboss_repo_from_yum":
    command => "/usr/bin/yum-config-manager --disablerepo jboss-repo",
    require => Package["jboss-eap-6.4"],
  }->
  notify { "jboss repo disabled": }

# remove new repo to yum part duex
#  yumrepo { "disable_jboss_repo_from_yum":
#    baseurl  => "file:///opt/myrepo/jboss-repo.repo",
#    descr    => "EAP 6 repository",
#    enabled  => 0,
#    gpgcheck => 0,
#  }

# stop eap yum
  service { "jboss-eap-6.4":
    ensure => "stopped",
  }

}
