%undefine       _disable_source_fetch
%define         gitname bthelper
%define         major 0
%define         minor 0
%define         build_timestamp %(date +"%Y%m%d")
%define         branch main
%define         console_service bluetooth-console.service
%define         ssh_service bluetooth-ssh.service
Name:           %{gitname}
Version:        %{major}.%{minor}~git_%{branch}
Release:        %{build_timestamp}
Group:          System/Management
Summary:        Helper program to SSH over bluetooth
License:        Apache-2.0
URL:            https://github.com/ThomasHabets/%{gitname}
Source:         %{url}/archive/refs/heads/%{branch}.zip
Source1:        %console_service
Source2:        %ssh_service
%systemd_requires

%description
This can be a useful second way in in case you have a
raspberry pi with broken network or firewall config.

%prep
%setup -q -n %{gitname}-%{branch}

%build
./bootstrap.sh
%configure
%make_build

%install
for service in console_service ssh_service; do
  install -D -m 0644 %{_sourcedir}/%{service} %{buildroot}%{_unitdir}/%{service}
done
%make_install

%pre
%service_add_pre %console_service %ssh_service

%post
%service_add_post %console_service %ssh_service

%preun
%service_del_preun %console_service %ssh_service

%postun
%service_del_postun %console_service %ssh_service

%files
/usr/bin/*
%{_unitdir}/%{console_service}
%{_unitdir}/%{ssh_service}
%license LICENSE
%doc README.md

%changelog
