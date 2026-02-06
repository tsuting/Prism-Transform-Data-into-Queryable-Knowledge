// Document Intelligence Resource
// Provides: Azure AI Document Intelligence for PDF/document extraction

@description('Location for resources')
param location string

@description('Tags to apply to resources')
param tags object = {}

@description('Name of the Document Intelligence account')
param name string

@description('SKU name')
@allowed(['F0', 'S0'])
param skuName string = 'S0'

// Document Intelligence is a Cognitive Services resource with kind 'FormRecognizer'
resource documentIntelligence 'Microsoft.CognitiveServices/accounts@2024-04-01-preview' = {
  name: name
  location: location
  tags: tags
  kind: 'FormRecognizer'
  identity: {
    type: 'SystemAssigned'
  }
  sku: {
    name: skuName
  }
  properties: {
    customSubDomainName: toLower(name)
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
  }
}

// Outputs
output name string = documentIntelligence.name
output id string = documentIntelligence.id
output endpoint string = documentIntelligence.properties.endpoint
output principalId string = documentIntelligence.identity.principalId
