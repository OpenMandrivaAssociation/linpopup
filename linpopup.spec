%define name linpopup
%define version 2.0.7
%define release %mkrel 2
%define prefix %_prefix

Summary: Linux enhanced port of winpopup
Name: %name
Version: %version
Release: %release
License: GPL
Group: Networking/Other
Source: http://prdownloads.sourceforge.net/linpopup2/%{name}-%{version}.tar.bz2
Source1: %{name}-16x16.png.bz2
Source2: %{name}-32x32.png.bz2
Source3: %{name}-48x48.png.bz2
#Patch:	 linpopup-2.0.1-fix-makefile.patch.bz2
URL:	http://linpopup2.sourceforge.net/
Prefix: %prefix
Requires: samba-client
BuildRequires: gtk2-devel automake libxmu-devel
Provides: LinPopUp = %{version}-%{release}
Obsoletes: LinPopUp

%description
LinPopUp is a Xwindow graphical port of Winpopup,
running over Samba. It permits to communicate with a
windows computer that runs Winpopup, sending or 
receiving message. (It also provides an alternative way
to communicate between Linux computers that run Samba).
Please note that LinPopUp is not only a port, as it includes
several enhanced features. Also note that it requires to
have Samba installed to be fully functionnal. 

To make this program work you have to add this line to your samba smb.conf
in the [global] section:

message command = %{_bindir}/LinPopUp "%%f" "%%m" %%s; rm %%s

%prep
%setup -q
#%patch -p1
perl -pi -e 's/ln -[a-z]+/install/g' Makefile.in
perl -pi -e 's/ln -[a-z]+/install/g' src/Makefile.in
for i in `find . -maxdepth 1 -type l`;do j=`readlink $i`;rm -f $i; cp $j $i;done

%build
%configure
%make DATA_DIR=%{_localstatedir}/%{name} DATA_FILE=%{_localstatedir}/%{name}/messages.dat

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
%makeinstall_std SHARE_DIR=%{_datadir}/%{name}

mkdir -p $RPM_BUILD_ROOT/var/lib/linpopup
#menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): \
command="%{_bindir}/%{name}" \
icon="%{name}.png" \
needs="X11" \
section="Internet/Instant Messaging" \
title="LinPopUp" \
longtitle="A Linux enhanced port of winpopup" \
xdg="true"
EOF

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=LinPopUp
Exec=%{_bindir}/%{name}
Icon=%{name}
Type=Application
Categories=GNOME;GTK;X-MandrivaLinux-Internet-InstantMessaging;Network;InstantMessaging;
EOF
#icons
install -d $RPM_BUILD_ROOT/%{_miconsdir}
install -d $RPM_BUILD_ROOT/%{_liconsdir}
install -d $RPM_BUILD_ROOT/%{_iconsdir}
bzcat %{SOURCE1} > $RPM_BUILD_ROOT/%{_miconsdir}/%{name}.png
bzcat %{SOURCE2} > $RPM_BUILD_ROOT/%{_iconsdir}/%{name}.png
bzcat %{SOURCE3} > $RPM_BUILD_ROOT/%{_liconsdir}/%{name}.png

rm -rf $RPM_BUILD_ROOT%_prefix/doc

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /var/lib/linpopup/messages.dat ]; then
    touch /var/lib/linpopup/messages.dat;
    chmod 0666 /var/lib/linpopup/messages.dat;
    chgrp nobody /var/lib/linpopup/messages.dat;
else :; fi;  
%{update_menus}

%postun
%{clean_menus}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS THANKS INSTALL TODO COPYING README MANUAL ChangeLog
%{_bindir}/LinPopUp
%{_bindir}/linpopup
%{_mandir}/man1/LinPopUp.1*
%{_mandir}/man1/linpopup.1*
%{_datadir}/%{name}
%{_menudir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%dir /var/lib/linpopup
/var/lib/linpopup/*
#%attr(0666,root,nobody) /var/lib/linpopup/*


