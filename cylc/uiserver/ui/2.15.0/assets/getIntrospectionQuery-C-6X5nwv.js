function e(e){let t={descriptions:!0,specifiedByUrl:!1,directiveIsRepeatable:!1,schemaDescription:!1,inputValueDeprecation:!1,experimentalDirectiveDeprecation:!1,oneOf:!1,typeDepth:9,...e},n=t.descriptions?`description`:``,r=t.specifiedByUrl?`specifiedByURL`:``,i=t.directiveIsRepeatable?`isRepeatable`:``,a=t.schemaDescription?n:``;function o(e){return t.inputValueDeprecation?e:``}function s(e){return t.experimentalDirectiveDeprecation?e:``}let c=t.oneOf?`isOneOf`:``;function l(e,t){if(e<=0)return``;if(e>100)throw Error(`Please set typeDepth to a reasonable value between 0 and 100; the default is 9.`);return`
${t}ofType {
${t}  name
${t}  kind${l(e-1,t+`  `)}
${t}}`}return`
    query IntrospectionQuery {
      __schema {
        ${a}
        queryType { name kind }
        mutationType { name kind }
        subscriptionType { name kind }
        types {
          ...FullType
        }
        directives${s(`(includeDeprecated: true)`)} {
          name
          ${n}
          ${i}
          ${s(`isDeprecated`)}
          ${s(`deprecationReason`)}
          locations
          args${o(`(includeDeprecated: true)`)} {
            ...InputValue
          }
        }
      }
    }

    fragment FullType on __Type {
      kind
      name
      ${n}
      ${r}
      ${c}
      fields(includeDeprecated: true) {
        name
        ${n}
        args${o(`(includeDeprecated: true)`)} {
          ...InputValue
        }
        type {
          ...TypeRef
        }
        isDeprecated
        deprecationReason
      }
      inputFields${o(`(includeDeprecated: true)`)} {
        ...InputValue
      }
      interfaces {
        ...TypeRef
      }
      enumValues(includeDeprecated: true) {
        name
        ${n}
        isDeprecated
        deprecationReason
      }
      possibleTypes {
        ...TypeRef
      }
    }

    fragment InputValue on __InputValue {
      name
      ${n}
      type { ...TypeRef }
      defaultValue
      ${o(`isDeprecated`)}
      ${o(`deprecationReason`)}
    }

    fragment TypeRef on __Type {
      kind
      name${l(t.typeDepth,`      `)}
    }
  `}export{e as t};