import React from 'react';
import { FormattedMessage } from 'react-intl';

import messages from './messages';
import { TaskSelectionIcon, AreaIcon, SubmitWorkIcon } from '../svgIcons';

function MappingCard({ image, title, description }: Object) {
  return (
    <div className="db ph2-l pb3 w-100">
      <div className="shadow-4 mh2 bg-white">
        <div className="pa1 ph3-m cf">
          <div className="red pv2 fl dib mr3">{image}</div>
          <h4 className="blue-dark b dib mt2 mb2">
            <FormattedMessage {...title} />
          </h4>
          <p className="blue-grey lh-copy db mt1">
            <FormattedMessage {...description} />
          </p>
        </div>
      </div>
    </div>
  );
}

export function NewMapperFlow() {
  const style = { height: '5rem', width: '6rem' };
  const cards = [
    {
      image: <TaskSelectionIcon style={style} />,
      title: messages.selectATaskCardTitle,
      description: messages.selectATaskCardDescription,
    },
    {
      image: <AreaIcon style={style} />,
      title: messages.mapThroughOSMCardTitle,
      description: messages.mapThroughOSMCardDescription,
    },
    {
      image: <SubmitWorkIcon style={style} />,
      title: messages.submitYourWorkCardTitle,
      description: messages.submitYourWorkCardDescription,
    },
  ];
  return (
    <div className="bg-white black cf">
      <div className="ph6-l ph4 pb3 w-100 w-70-l fl bg-split-white-grey-light">
        {cards.map((card, n) => (
          <MappingCard {...card} key={n} />
        ))}
      </div>
      <div className="w-30-l fl dn dib-l bg-white"></div>
    </div>
  );
}
