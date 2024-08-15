import requests
from rich.console import Console

console = Console()

cms_signatures = {
    cms_signatures = {
    'WordPress': ['wp-content', 'wp-includes', 'xmlrpc.php'],
    'Joomla': ['Joomla!', 'index.php?option=com_', 'Joomla User Login'],
    'Drupal': ['sites/default/files', 'drupal.js', 'user/login'],
    'Magento': ['mage/', 'skin/frontend', 'Magento, Inc.'],
    'TYPO3': ['typo3/', 't3lib/', 'index.php?id='],
    'Shopify': ['cdn.shopify.com', 'shopify-checkout-api', 'shopify_payments_account_id'],
    'PrestaShop': ['PrestaShop', 'ps_', 'var prestashop'],
    'OpenCart': ['catalog/view/theme/', 'index.php?route=', 'OpenCart'],
    'Wix': ['wix.com', '_wix/', 'wixstatic.com'],
    'Squarespace': ['squarespace.com', 'static.squarespace.com', 'squarespace-settings'],
    'Ghost': ['ghost/', 'content/themes/', 'ghost.org'],
    'ExpressionEngine': ['ExpressionEngine', 'exp:channel:entries', 'exp:channel:form'],
    'osCommerce': ['osCommerce', 'index.php?cPath=', 'osCommerce Online Merchant'],
    'Blogger': ['blogspot.com', 'blogger.com', 'blogger.googleusercontent.com'],
    'Bitrix': ['bitrix/', 'bitrix/js/', 'bitrix/tools/'],
    'DotNetNuke': ['dnn', 'DotNetNuke', '/portals/'],
    'Sitefinity': ['Telerik.Sitefinity', 'sitefinity', 'sitefinitycms'],
    'BigCommerce': ['cdn11.bigcommerce.com', 'bigcommerce.com', 'bc-sf-filter'],
    'Zen Cart': ['zencart/', 'index.php?main_page=', 'zenid'],
    'SilverStripe': ['SilverStripe', 'framework/', 'SilverStripeNavigator'],
    'Craft CMS': ['craft/', 'craftcms', 'craft/assets/'],
    'Concrete5': ['concrete5', 'concrete/css/', 'concrete/js/'],
    'Weebly': ['weebly.com', 'weeblycloud.com', 'editmysite.com'],
    'Umbraco': ['umbraco', 'Umbraco.', 'umbraco/umbraco.js'],
    'MODX': ['MODX', 'manager/index.php?a=', 'modx-sitecheck'],
    'Contentful': ['contentful', 'cdn.contentful.com', 'contentful.com'],
    'Webflow': ['webflow.com', 'wf-assets/', 'Webflow requires JavaScript'],
    'Liferay': ['liferay', 'web/guest', 'group/control_panel'],
    'vBulletin': ['vbulletin', 'vBulletin', 'forumdisplay.php'],
    'MediaWiki': ['mediawiki', 'index.php?title=', 'Special:Version'],
    'TYPOlight': ['TYPOlight', 'tl_files', 'index.php?user'],
    'CMS Made Simple': ['CMS Made Simple', 'tmp/cache', 'CMSMS'],
    'phpBB': ['phpbb', 'phpBB', 'viewforum.php'],
    'XenForo': ['xenforo', 'XenForo', 'community/scripts/'],
    'Textpattern': ['textpattern', 'rpc.php', 'textpattern.js'],
    'Simple Machines Forum (SMF)': ['smf_', 'Simple Machines Forum', 'index.php?action='],
    'ExpressionEngine': ['ExpressionEngine', 'exp:channel:entries', 'exp:channel:form'],
    'Serendipity': ['serendipity', 'serendipity.css', 'serendipity_config_local.inc.php'],
    'Dotclear': ['dotclear', 'dotclear/index.php', 'themes/dotclear/'],
    'e107': ['e107_', 'e107_files', 'e107_admin/'],
    'PivotX': ['pivotx', 'pivotx', 'pivotx-admin'],
    'PostNuke': ['postnuke', 'pnadmin.php', 'modules/NS-User/'],
    'phpNuke': ['phpnuke', 'mainfile.php', 'modules.php?name='],
    'XOOPS': ['xoops', 'xoops.css', 'modules/system/'],
    'Movable Type': ['mt-static', 'movabletype', 'mt.cgi'],
    'Plone': ['plone', 'portal_css', 'portal_javascripts'],
    'Nucleus CMS': ['nucleus', 'nucleus/css', 'action.php?'],
    'BlogEngine.NET': ['blogengine', 'admin/default.aspx', 'BlogEngine.Core'],
    'Exponent CMS': ['exponent', 'themes/exponent/'],
    'OpenCMS': ['opencms', 'system/workplace/', 'opencms/opencms/'],
    'Geeklog': ['geeklog', 'index.php?topic=', 'lib-common.php'],
    'Subrion CMS': ['subrion', 'modules/subrion/', 'admin_panel/js/'],
    'Grav CMS': ['grav', 'user/themes/', 'system/grav-admin/'],
}

}

def detect_cms(url):


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    try:
        response = requests.get(url,headers=headers)
        for cms, signatures in cms_signatures.items():
            if any(signature in response.text for signature in signatures):
                console.print(f"[green]CMS detected: {cms}[/green]")
                return f"CMS detected for {url}: {cms}"
        return f"No CMS detected for {url}"
    except requests.ConnectionError:
        return f"Could not connect to {url}"

# Example usage
if __name__ == "__main__":
    target_url = "https://www.tapidiploma.org"
    detect_cms(target_url)
