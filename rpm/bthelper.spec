%undefine       _disable_source_fetch
%define         gitname bthelper
%define         major 0
%define         minor 0
%define         build_timestamp %(date +"%Y%m%d")
%define         branch main
%define         systemd_service bluetooth-ssh.service
Name:           %{gitname}
Version:        %{major}.%{minor}~git_%{branch}
Release:        %{build_timestamp}
Group:          System/Management
Summary:        Helper program to SSH over bluetooth
License:        Apache-2.0
URL:            https://github.com/twojstaryzdomu/%{gitname}
Source:         %{url}/archive/refs/heads/%{branch}.zip
Source1:        %systemd_service
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
install -D -m 0644 %{_sourcedir}/%{systemd_service} %{buildroot}%{_unitdir}/%{systemd_service}
%make_install

%pre
%service_add_pre %systemd_service

%post
%service_add_post %systemd_service

%preun
%service_del_preun %systemd_service

%postun
%service_del_postun %systemd_service

%files
/usr/bin/*
%{_unitdir}/%{systemd_service}
%license LICENSE
%doc README.md

%changelog
