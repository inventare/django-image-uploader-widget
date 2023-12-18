import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

const VersionsPage = () => {
  return (
    <Layout
      title="Versions"
      description="Docusaurus 2 Versions page listing all documented site versions"
    >
      <main className="container margin-vert--lg">
        <h1>Image-Uploader-Widget Versions</h1>

        <div className="margin-bottom--lg">
          <h3>
            Current version (Stable)
          </h3>
          <p>
            Here you can find the documentation for current released version.
          </p>
          <table>
            <tbody>
              <tr>
                <th>0.4.1</th>
                <td>
                  <Link to="/docs/intro/">
                    Documentation
                  </Link>
                </td>
                <td>
                  Introduced <code>OrderedImageUploaderInline</code>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="margin-bottom--lg">
          <h3>
            Past versions (Not maintained anymore)
          </h3>
          <p>
          Here you can find documentation for previous versions.
          </p>
          <table>
            <tbody>
              <tr>
                <th>0.4.0</th>
                <td>
                  <Link to="/docs/0.4.0/intro/">
                    Documentation
                  </Link>
                </td>
                <td>
                  Support for Django 5.0
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </main>
    </Layout>
  );
}

export default VersionsPage;
