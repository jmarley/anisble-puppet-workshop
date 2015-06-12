class remove_eap6 {

  file { '/opt/myrepo/':
    path    => '/opt/myrepo/',
    ensure  => absent, 
    recurse => true,
    purge   => true,
    force   => true,
  }


}
