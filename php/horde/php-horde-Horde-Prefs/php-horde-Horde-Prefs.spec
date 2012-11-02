%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Prefs

Name:           php-horde-Horde-Prefs
Version:        1.1.8
Release:        1%{?dist}
Summary:        Horde Preferences API

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.7.0
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(pear.horde.org/%{pear_name}) = %{version}
Requires:       php-pear(pear.horde.org/Horde_Exception) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Mime) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Translation) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Util) < 2.0.0
Requires:       php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(pear.horde.org)
Requires:       php-channel(pear.horde.org)

%description
The Horde_Prefs package provides a common abstracted interface into the
various preferences storage mediums. It also includes all of the functions
for retrieving, storing, and checking preference values.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml

# Create a "localized" php.ini to avoid build warning
cp /etc/php.ini .
echo "date.timezone=UTC" >>php.ini

cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
PHPRC=../php.ini %{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}

%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.horde.org/%{pear_name} >/dev/null || :
fi

%files
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Prefs
%{pear_phpdir}/Horde/Prefs.php
%{pear_datadir}/Horde_Prefs
%{pear_testdir}/Horde_Prefs
%{_bindir}/horde-prefs

%changelog
* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.8-1
- Upgrade to 1.1.8

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.7-1
- Initial package
