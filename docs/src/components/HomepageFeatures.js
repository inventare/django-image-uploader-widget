import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Beautiful',
    image: require('../../static/img/beautiful.gif').default,
    description: (
      <>
        The <strong>django-image-uploader-widget</strong> is a beautiful widget for handling 
        image uploads in django forms, specially in django-admin.
      </>
    ),
  },
  {
    title: 'Multiple Images Handling',
    image: require('../../static/img/inline_multiple.gif').default,
    description: (
      <>
        The <strong>django-image-uploader-widget</strong> includes an inline editor
        to handle multiple images uploading.
      </>
    ),
  },
  {
    title: 'Support Both Click and Drag and Drop Behaviours',
    image: require('../../static/img/click.gif').default,
    description: (
      <>
        The <strong>django-image-uploader-widget</strong> includes both behaviours
        support: <strong>click to select image</strong> or <strong>drag and drop image</strong>.
      </>
    ),
  },
];

function Feature({image, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <img src={image} className={styles.featureImage} />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
