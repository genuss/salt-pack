%define tarballname yaml

#====================================================================#

Name:       libyaml
Version:    0.1.3
Release:    4%{?dist}
Summary:    YAML 1.1 parser and emitter written in C

Group:      System Environment/Libraries
License:    MIT
URL:        http://pyyaml.org/
Source0:    http://pyyaml.org/download/libyaml/%{tarballname}-%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: autoconf, automake, libtool

# CVE-2013-6393
# https://bugzilla.redhat.com/show_bug.cgi?id=1033990
Patch0:     libyaml-CVE-2013-6393-string-overflow.patch
Patch1:     libyaml-CVE-2013-6393-node-id-hardening.patch
Patch2:     libyaml-CVE-2013-6393-indent-and-flow-overflow-1-of-3.patch
Patch3:     libyaml-CVE-2013-6393-indent-and-flow-overflow-2-of-3.patch
Patch4:     libyaml-CVE-2013-6393-indent-and-flow-overflow-3-of-3.patch
Patch5:     libyaml-CVE-2014-2525-URL-buffer-overflow.patch
Patch6:     libyaml-CVE-2014-9130.patch

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  LibYAML is a YAML parser and
emitter written in C.


%package devel
Summary:   Development files for LibYAML applications
Group:     Development/Libraries
Requires:  libyaml = %{version}-%{release}


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use LibYAML.


%prep
%setup -q -n %{tarballname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
autoreconf -i -f
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} INSTALL="install -p" install
rm -f %{buildroot}%{_libdir}/*.{la,a}

soname=$(readelf -d %{buildroot}%{_libdir}/libyaml.so | awk '$2 == "(SONAME)" {print $NF}' | tr -d '[]')
rm -f %{buildroot}%{_libdir}/libyaml.so
echo "INPUT($soname)" > %{buildroot}%{_libdir}/libyaml.so


%check
make check


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LICENSE README
%{_libdir}/%{name}*.so.*


%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_libdir}/%{name}*.so
%{_includedir}/yaml.h


%changelog
* Mon Dec 15 2014 John Eckersberg <eck@redhat.com> - 0.1.3-4
- Add patch for CVE-2014-9130 (RHBZ#1169369)

* Mon Mar 31 2014 John Eckersberg <jeckersb@redhat.com> - 0.1.3-1.4
- Work around ldconfig bug with libyaml.so (bz1082822)

* Mon Mar 24 2014 John Eckersberg <jeckersb@redhat.com> - 0.1.3-1.3
- Add patch for CVE-2014-2525 (bz1078083)

* Mon Mar 24 2014 John Eckersberg <jeckersb@redhat.com> - 0.1.3-1.2
- Add patches for CVE-2013-6393 (bz1033990)

* Tue Sep 11 2012 Alan Pevec <apevec@redhat.com> 0.1.3-1.1
- Import into RHEL 6.4 (rhbz#851796)

* Fri Oct 02 2009 John Eckersberg <jeckersb@redhat.com> - 0.1.3-1
- New upstream release 0.1.3

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 John Eckersberg <jeckersb@redhat.com> - 0.1.2-4
- Minor tweaks to spec file
- Enable %%check section
- Thanks Gareth Armstrong <gareth.armstrong@hp.com>

* Tue Mar 3 2009 John Eckersberg <jeckersb@redhat.com> - 0.1.2-3
- Remove static libraries

* Thu Feb 26 2009 John Eckersberg <jeckersb@redhat.com> - 0.1.2-2
- Remove README and LICENSE from docs on -devel package
- Remove -static package and merge contents into the -devel package

* Wed Feb 25 2009 John Eckersberg <jeckersb@redhat.com> - 0.1.2-1
- Initial packaging for Fedora
