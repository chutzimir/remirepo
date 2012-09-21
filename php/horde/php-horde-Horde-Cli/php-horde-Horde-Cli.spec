%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Cli

Name:           php-horde-Horde-Cli
Version:        1.0.4
Release:        2%{?dist}
Summary:        Horde Command Line Interface API

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz
# /usr/lib/rpm/find-lang.sh from fedora 16
Source1:        find-lang.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php-pear >= 1.7.0
BuildRequires:  php-channel(pear.horde.org)
BuildRequires:  gettext

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(pear.horde.org/Horde_Support) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Translation) < 2.0.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(pear.horde.org)
Requires:       php-pcre php-session
Requires:       php-common >= 5.2.0

Provides:       php-pear(pear.horde.org/%{pear_name}) = %{version}

%description
Horde_Cli:: API for basic command-line functionality/checks

%prep
%setup -q -c

# Create a "localized" php.ini to avoid build warning
cp /etc/php.ini .
echo "date.timezone=UTC" >>php.ini

cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}.po/d' \
    -e '/%{pear_name}.mo/s/md5sum=.*name=/name=/' \
    ../package.xml >%{name}.xml

%build
cd %{pear_name}-%{version}

# Regenerate the locales
for po in $(find locale -name \*.po)
do
   msgfmt $po -o $(dirname $po)/$(basename $po .po).mo
done

%install
cd %{pear_name}-%{version}
PHPRC=../php.ini %{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}
%if 0%{?fedora} > 13 || 0%{?rhel} > 6
%find_lang %{pear_name}
%else
sh %{SOURCE1} $RPM_BUILD_ROOT %{pear_name}
%endif

%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.horde.org/%{pear_name} >/dev/null || :
fi

%files -f %{pear_name}-%{version}/%{pear_name}.lang
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Cli
%{pear_phpdir}/Horde/Cli.php
# own locales (non standard) directories, .mo own by find_lang
%dir %{pear_datadir}/Horde_Cli
%dir %{pear_datadir}/Horde_Cli/locale
%dir %{pear_datadir}/Horde_Cli/locale/*
%dir %{pear_datadir}/Horde_Cli/locale/*/LC_MESSAGES

%changelog
* Thu Sep 20 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.4-2
- backport for remi repo

* Mon Jun 25 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.4-2
- Fix requires

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.4-1
- Initial package