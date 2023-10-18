import React from 'react';
import Head from '@docusaurus/Head';

function PageTitle({title}) {
  return (
    <Head>
      <title>{title}</title>
    </Head>
  );
}

export default PageTitle;